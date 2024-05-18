# Incrementally Computing the Hypervolume of a Set of n-D Points for n=3 and 4
This repository contains the description and corresponding files for the " Incrementally computing the hypervolume of a set of n-D points for n=3 and 4" project.

This is a project for the master's subject "Matematika z računalnikom" at University of Ljubljana, Faculty of Mathematics and Physics. 

## Description
The hypervolume of a set of n-D points is often used in multi-objective optimization and serves as a measure of tracking the progress of optimization algorithms.

The goal of this project is to transfer the most computationally efficient implementation of the incremental hypervolume computation for 3-D and 4-D spaces, which is written in C, into Python.

## Repository Structure
The repository is structured as follows:
- The *moarchiving* folder consists of my implementation of the hypervolume problem in three and four dimensions in Python. The `hv_plus.py` contains all the auxiliary funtions as well as the main function for computing the hypervolume in both three and four dimensions. Example tests for all the functions are written in the `hv_plus_tests.py` file, which can be run by simply downloading both files into the same folder and then running the `hv_plus_tests.py` file.
- The *related* folder is a copy of the `HVC` repository, available on [https://github.com/apguerreiro/HVC]. Here, the original implementation is available as well as example cases.
