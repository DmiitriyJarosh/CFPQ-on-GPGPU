# fast boolean semiring matrix multiplication for CFPQ

## Implementations

* CPU:
  * matrix multiplication using m4ri lib
  * sparse boolean matrix multiplication using libs on Python
* GPU:
  * naive matrix multiplication with packed into uint32 boolean values
  * Four Russians method for matrix multiplication with packed into uint32 boolean values

## Documentation

1. Environment  
All tests should run inside docker, so first of all you build image via `Dockerfile` in root folder. We use `ubuntu 18.04` with `CUDA` compability as main image and install `anaconda`, `mono`, `m4ri library` and some usefull utilites.  
Builded image has `CMD` command for automatic testing, when it starts, so you should mount folder with all data and generate test data to `tests.csv`.  
For example, if your data stores in `data` folder, run docker with this command:  

```(bash)
docker run -v /<path to project>/data:/data/ <image name>
```

2. Tests preparation  
Because of large files, we use `git lfs` for storing all data, install it and then you can pull repository with all data files without any other movements. For testing system we use `tests.csv` file with describing all tests, we need it because differents tests may use same files, you can't run testing **without** this file. For creating this file you can use `test_utils/build_testset.py` script, it has only parameter ‒ path to folder with data.  
For example, if your data stores in `data` folder, run this command for generate tests description:

```(bash)
python test_utils/build_testset.py data
```
