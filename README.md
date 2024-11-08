# MOArchiving
This work extends the [moarchiving](https://github.com/CMA-ES/moarchiving) library to work in 3 and 
4 dimensions. For efficient implementation of hypervolume calculation in 3 and 4 dimensions, 
we follow the approach described in "Computing and Updating Hypervolume Contributions in Up to 
Four Dimensions" by A. P. Guerreiro and C. M. Fonseca, which is described and implemented in 
C code [here](https://github.com/apguerreiro/HVC). We rewrite this implementation in python and
add all the other functions that are available in 2D in the original moarchiving library.

### Authors:
- Mila Nedić
- Nace Sever
