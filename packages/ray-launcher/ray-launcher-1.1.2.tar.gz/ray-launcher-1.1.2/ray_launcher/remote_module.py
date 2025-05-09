import os
import ray
import inspect

from collections import namedtuple
from typing import Optional, List
from functools import partial
from loguru import logger
from ray.util.scheduling_strategies import PlacementGroupSchedulingStrategy

from .base_local_module import BaseLocalModule

PlacementGroupAndIndex = namedtuple("PlacementGroupAndIndex", ["placement_group", "bundle_index"])

class RemoteModule:
    def __init__(
            self, 
            backend_clz,
            placement_groups_and_indices: list[PlacementGroupAndIndex],
            discrete_gpu_actors: Optional[bool] = False, # must be gpu actor first, cpu actor is not discrete
            backend_actor_kwargs: Optional[dict] = None,
            export_env_var_names: Optional[List] = None,
            do_not_set_cuda_visible_devices: bool = False,
            module_name: Optional[str] = None
    ):
        self.backend_clz = backend_clz
        assert issubclass(self.backend_clz, BaseLocalModule)
        if module_name is None:
            module_name = backend_clz.__name__ + str(id(self))
        self.module_name = module_name

        self.discrete_gpu_actors = discrete_gpu_actors
        
        self.backend_actors = []
        if export_env_var_names is None:
            export_env_var_names = []
        if backend_actor_kwargs is None:
            backend_actor_kwargs = {}
        self._create_backend_actors(
            placement_groups_and_indices, 
            do_not_set_cuda_visible_devices,
            export_env_var_names,
            backend_actor_kwargs
        )


        self._register_remote_funcs()

    
    def _create_backend_actors(
            self,
            placement_groups_and_indices: List[PlacementGroupAndIndex], 
            do_not_set_cuda_visible_devices: bool,
            export_env_var_names: List,
            backend_actor_kwargs: dict,
        ):
        env_vars = {}
        for name in export_env_var_names:
            if name in os.environ:
                env_vars.update(
                    {name: os.environ.get(name)}
                )
            else:
                logger.warning(f"{name} does not exist in environ")
        if do_not_set_cuda_visible_devices is True:
             env_vars.update({"RAY_EXPERIMENTAL_NOSET_CUDA_VISIBLE_DEVICES": "1"})

        if self.discrete_gpu_actors is True:
            for pg, idx in placement_groups_and_indices:
                current_bundle_gpu_count = int(pg.bundle_specs[idx].get("GPU"))
                assert current_bundle_gpu_count > 0, f"discrete gpu actor must be created on group with gpu resource"
                current_bundle_cpu_count_per_gpu = float(pg.bundle_specs[idx].get("CPU"))/current_bundle_gpu_count
                for _ in range(current_bundle_gpu_count):
                    remote_actor = ray.remote(
                            num_gpus=1,
                            num_cpus=current_bundle_cpu_count_per_gpu
                        )(self.backend_clz).options(
                            scheduling_strategy=PlacementGroupSchedulingStrategy(
                                placement_group=pg,
                                placement_group_bundle_index=idx,
                        ) , runtime_env={"env_vars": env_vars}
                        ).remote(**backend_actor_kwargs)
                    self.backend_actors.append(remote_actor)
                    logger.debug(f"created discrete GPU remote actor {len(self.backend_actors) - 1} of module {self.module_name} (args: {backend_actor_kwargs})" 
                                 f"on {pg.id} idx={idx} with 1 gpu, {current_bundle_cpu_count_per_gpu} cpu and environ {env_vars}")

            assert len(self.backend_actors) > 0
            rank_0_actor = self.backend_actors[0]
            module_master_addr = ray.get(rank_0_actor.get_ip_address.remote())
            module_master_port = ray.get(rank_0_actor.get_avaiable_port.remote())
            logger.debug(f"rank 0 backend gives {module_master_addr=}, {module_master_port=}")

            set_environs_futures = []
            for actor_idx, actor in enumerate(self.backend_actors):
                set_environs_futures.append(actor.set_distributed_environs.remote(
                    actor_idx,
                    len(self.backend_actors),
                    module_master_addr,
                    module_master_port
                ))
            ray.get(set_environs_futures)


        else:
            assert len(placement_groups_and_indices) == 1, f"the actor is continuous, should not spread to groups"
            pg, idx = placement_groups_and_indices.pop()
            current_bundle_gpu_count = int(pg.bundle_specs[idx].get("GPU", 0))
            current_bundle_cpu_count = int(pg.bundle_specs[idx].get("CPU", 0))
            self.backend_actors.append(
                ray.remote(
                    num_gpus=current_bundle_gpu_count,
                    num_cpus=current_bundle_cpu_count
                )(self.backend_clz).options(
                    scheduling_strategy=PlacementGroupSchedulingStrategy(
                        placement_group=pg,
                        placement_group_bundle_index=idx,
                ), runtime_env={"env_vars": env_vars}
                ).remote(**backend_actor_kwargs)
            )
            logger.debug(f"created single continuous GPU/CPU remote actor of module {self.module_name} (args={backend_actor_kwargs}) on "
                         f"{pg.id} idx={idx} with {current_bundle_gpu_count} gpu, {current_bundle_cpu_count} cpu and environ {env_vars}")

    

    def _call_func_of_all_remote_actors(self, func_name: str, *args, **kwargs):
        all_func_returns = []
        for actor in self.backend_actors:
            assert hasattr(actor, func_name)
            all_func_returns.append(getattr(actor, func_name).remote(*args, **kwargs))
        if len(all_func_returns) == 1:
            all_func_returns = all_func_returns[0]
        else:
            logger.debug(f"module {self.module_name} contains multiple actors, will return a list of all results")
        return ray.get(all_func_returns)
    
    
    def _register_remote_funcs(self):
        self.remote_funcs = []
        for name, member in inspect.getmembers(self.backend_clz, predicate=inspect.isfunction):
            if not name.startswith("__"): # auto register all non-magic methods
                self.remote_funcs.append(name)
                setattr(self, name, partial(self._call_func_of_all_remote_actors, name))
                logger.debug(f"auto detected and registered remote func: {name}({member})")

