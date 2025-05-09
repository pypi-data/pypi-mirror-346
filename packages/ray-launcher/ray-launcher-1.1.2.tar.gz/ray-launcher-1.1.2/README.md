# Ray Launcher

## Introduction

`ray-launcher` is an out-of-the-box python library that wraps the frequently used `ray`  practices enabling migrating from local classes and starting ray cluster with minimum amount of code.

## Updates 

- v1.1.2: add support for actor init kwargs, fix 0 GPU case, refactored `BaseBackend` as `BaseLocalModule`
- v1.1.1: add option of not setting cuda devices when creating backend actors
- v1.1.0: `RemoteModule` provides the wrap for fast converting local class to ray remote class
- v1.0.1: fixed problem of exiting with 1 node 
- v1.0.0: `ClusterLauncher` that wraps dirty scripts and spin waits on multi nodes

## Features


### `ClusterLauncher`

This ray cluster launcher wraps the following steps internally:

- run `ray start` commands on head and worker noodes
- run `ray.init` on all nodes
- head node spin wait for all nodes to start
- cluster start after all nodes joined
- head node returns context to main code while worker nodes spin waits for cluster to be torn down
- worker node run `ray.shutdown` and `ray stop` command after cluster starting to be torn down
- head exits after all worker nodes exited successfully

### `RemoteModule`

This is the wrap of `ray.remote` and commonly used actor creation steps:

- create remote actor of given backend class (if `discrete_gpu_actors is True`, create actors of the same amount of gpus in the reserved resources)
- export environs for distributed computing if `discrete_gpu_actors is True`, including `"RANK", "WORLD_SIZE", "MASTER_ADDR", "MASTER_PORT", "LOCAL_RANK"`
- auto detect and export the remote funcs of backend class to remote module itself

note: (1) the backend class must inherit from `BaseLocalModule` (2) the auto export remote funcs returns a list of results of all backend actors if `discrete_gpu_actors is True` 

## Quick Start

step1: install
```bash
pip install ray-launcher
```


step2: change local class
```python
class YourLocalModuleClass(BaseLocalModule):
    def some_method(self):
        # ...
```

step3: start cluster and use remote module
```python
from ray_launcher import ClusterLauncher

with ClusterLauncher(
    cluster_nodes_count=int(os.environ["NNODES"]),
    head_node_addr=os.environ["MASTER_ADDR"],
) as launcher:

    bundle = [{"GPU": 2, "CPU": 32}, {"GPU": 2, "CPU": 32}]
    pg = ray.util.placement_group(bundle, strategy="PACK")
    module1 = RemoteModule(YourLocalModuleClass, [(pg, 0)], discrete_gpu_actors=True)
    module2 = RemoteModule(YourLocalModuleClass, [(pg, 1)], discrete_gpu_actors=False)

    print(module1.some_method()) # this will get a list of results of calling each backend actor
    print(module2.some_method()) # this will get one single result, since there is only one backend actor

    # write other code for head node to execute

```

For example, see: `test.py` or my other repository uses this lib: [LMarhsal](https://github.com/0-1CxH/LMarhsal)

