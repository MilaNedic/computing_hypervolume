# Introduction

This library implements a multi-objective (2, 3 and 4 objectives are supported) non-dominated archive. It provides easy and fast access to the hypervolume and hypervolume plus indicators, the contributing hypervolume of each element, and to the [uncrowded hypervolume improvement](https://arxiv.org/abs/1904.08823) of any given point in objective space.

Additionally, it provides a constrained version of the archive, which allows to store points with constraints and to compute the [ICMOP](https://arxiv.org/abs/2302.02170) indicator. 

## Installation

Either via
```
pip install git+https://github.com/CMA-ES/moarchiving.git@master
```

or simply via

```
pip install moarchiving
```

## Testing

```
python -m moarchiving.test
```

on a system shell should output something like

```
doctest.testmod(<module 'moarchiving.moarchiving2d' from '...\\moarchiving\\moarchiving2d.py'>)
TestResults(failed=0, attempted=90)

...

OK
unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromModule(<module 'moarchiving.tests.test_sorted_list' from '...\\moarchiving\\tests\\test_sorted_list.py'>))
.......
----------------------------------------------------------------------
Ran 7 tests in 0.001s
```

## Details

`moarchiving` uses the [`fractions.Fraction`](https://docs.python.org/3/library/fractions.html) type to avoid rounding errors when computing hypervolume differences, but its usage can also easily switched off by assigning the respective class attributes `hypervolume_computation_float_type` and `hypervolume_final_float_type`.

## Links

- [Code on Github](https://github.com/CMA-ES/moarchiving)
- Documentation (possibly slighly outdated) in
  - [this page plus performance test examples](https://cma-es.github.io/moarchiving/)
  - [apidocs format](https://cma-es.github.io/moarchiving/moarchiving-apidocs/index.html)
  - [epydocs format](https://cma-es.github.io/moarchiving/moarchiving-epydocs/index.html)

## Releases
- TODO: what is the current version?
- 0.7.0 reimplementation of `BiobjectiveNondominatedSortedList.hypervolume_improvement` by extracting a sublist first.
- 0.6.0 the `infos` attribute is a `list` with corresponding (arbitrary) information, e.g. for keeping the respective solutions.
- 0.5.3 fixed assertion error when not using `fractions.Fraction`
- 0.5.2 first published version

# Usage examples:

### Initialization of `MOArchive` for 2, 3 and 4 objectives
MOArchive object can be created using `get_archive` function providing a list of objective values, reference point or at least the number of objectives. Note that additional points can always be added using `add` or `add_list` functions, but reference point can not be changed once the object is initialized. A list of information strings can be provided for each point, which will be stored as long as the corresponding point stays in the archive (e.g. the x values used to generate the objective values). At any point the list of non-dominated points and their corresponding infos can be accessed. 


```python
from moarchiving.get_archive import get_mo_archive, get_cmo_archive
```


```python
# Creating a 2-objective archive
moa2d = get_mo_archive([[1, 5], [2, 3], [4, 5], [5, 0]], reference_point=[10, 10], infos=["a", "b", "c", "d"])
print("points in the archive:", list(moa2d))
print("infos of the corresponding points:", moa2d.infos)
```

    points in the archive: [[1, 5], [2, 3], [5, 0]]
    infos of the corresponding points: ['a', 'b', 'd']
    


```python
# Creating a 3-objective archive
moa3d = get_mo_archive([[1, 2, 3], [3, 2, 1], [3, 3, 0], [2, 2, 1]], [10, 10, 10], ["a", "b", "c", "d"])
print("points in the archive:", list(moa3d))
print("infos of the corresponding points:", moa3d.infos)
```

    points in the archive: [[3, 3, 0], [2, 2, 1], [1, 2, 3]]
    infos of the corresponding points: ['c', 'd', 'a']
    


```python
# creating a 4-objective archive
moa4d = get_mo_archive([[1, 2, 3, 4], [1, 3, 4, 5], [4, 3, 2, 1], [1, 3, 0, 1]], 
                       reference_point=[10, 10, 10, 10], infos=["a", "b", "c", "d"])
print("points in the archive:", list(moa4d))
print("infos of the corresponding points:", moa4d.infos)
```

    points in the archive: [[1, 3, 0, 1], [1, 2, 3, 4]]
    infos of the corresponding points: ['d', 'a']
    

### Constrained MOArchive
Constrained MOArchive supports all the functionalities of a non-constrained MOArchive, with the additional handling of constraints when adding or initializing the archive (next to the objectives of a point we need to add the constraints in form of a list or a number). 


```python
# creating 3-objective archive with constraints
cmoa = get_cmo_archive([[1, 2, 3], [1, 3, 4], [4, 3, 2], [1, 3, 0]], [[3, 0], [0, 0], [0, 0], [0, 1]], 
                         reference_point=[5, 5, 5], infos=["a", "b", "c", "d"])
print("points in the archive:", list(cmoa))
print("infos of the corresponding points:", cmoa.infos)
```

    points in the archive: [[4, 3, 2], [1, 3, 4]]
    infos of the corresponding points: ['c', 'b']
    

### Initializing empty archive and adding points
MoArchive can also be initialized empty, but at minimum the reference point or the number of objectives should be provided.


```python
moa = get_mo_archive(reference_point=[4, 4, 4])
print("points in the archive:", list(moa))

# add one point
moa.add([1, 2, 3], "a")
print("points:", list(moa))
print("infos:", moa.infos)

# add another point
moa.add([3, 2, 1], "b")
print("points:", list(moa))
print("infos:", moa.infos)

# add a dominated point (should not be added)
moa.add([3, 3, 3], "c")
print("points:", list(moa))
print("infos:", moa.infos)

moa.add_list([[2, 1, 3], [1, 3, 2], [3, 2, 0], [2, 2, 4]], ["d", "e", "f", "g"])
print("points:", list(moa))
print("infos:", moa.infos)
```

    points in the archive: []
    points: [[1, 2, 3]]
    infos: ['a']
    points: [[3, 2, 1], [1, 2, 3]]
    infos: ['b', 'a']
    points: [[3, 2, 1], [1, 2, 3]]
    infos: ['b', 'a']
    points: [[3, 2, 0], [1, 3, 2], [2, 1, 3], [1, 2, 3]]
    infos: ['f', 'e', 'd', 'a']
    

### List like interface
The MOArchive implements some functionality of a list (In 2D case it actually extends the list class, but this is not the case in 3 and 4D), in particular the `len` method to get the number of points in the archive as well as the `in` keyword to check if a point is in the archive.


```python
print("Points in the archive:", list(moa))
print("Length of the archive:", len(moa))
print("[2, 2, 2] in moa:", [2, 2, 2] in moa)
print("[3, 2, 0] in moa:", [3, 2, 0] in moa)
```

    Points in the archive: [[3, 2, 0], [1, 3, 2], [2, 1, 3], [1, 2, 3]]
    Length of the archive: 4
    [2, 2, 2] in moa: False
    [3, 2, 0] in moa: True
    

### Performance indicators
In order that all the performance indicators are easily comparable, we define all of them as a maximization indicators (by multiplying hypervolume plus and icmop indicators with -1). In that case when the archive is not empty, all the indicators are positive and have the same value. 

Accessing the hypervolume of the archive is done using the `hypervolume` attribute or the `hypervolume_plus` attribute for the hypervolume plus indicator. 


```python
print("Hypervolume of the archive:", moa.hypervolume)
print("Hypervolume plus of the archive:", moa.hypervolume_plus)
```

    Hypervolume of the archive: 16
    Hypervolume plus of the archive: 16
    

In case of a constrained MOArchive the `icmop` attribute can be accessed as well. 


```python
print("Hyperolume of the constrained archive:", cmoa.hypervolume)
print("Hypervolume plus of the constrained archive:", cmoa.hypervolume_plus)
print("Icmop of the constrained archive:", cmoa.icmop)
```

    Hyperolume of the constrained archive: 12
    Hypervolume plus of the constrained archive: 12
    Icmop of the constrained archive: 12.0
    

### Copying an archive


```python
moa_copy = moa.copy()
print("moa     ", list(moa))
print("moa_copy", list(moa_copy))

moa.add([1, 1, 1])
print("\nafter adding to the original archive:")
print("moa     ", list(moa))
print("moa_copy", list(moa_copy))
```

    moa      [[3, 2, 0], [1, 3, 2], [2, 1, 3], [1, 2, 3]]
    moa_copy [[3, 2, 0], [1, 3, 2], [2, 1, 3], [1, 2, 3]]
    
    after adding to the original archive:
    moa      [[3, 2, 0], [1, 1, 1]]
    moa_copy [[3, 2, 0], [1, 3, 2], [2, 1, 3], [1, 2, 3]]
    

### Contributing hypervolumes
Returns a list of contributions for each point of the archive. Alternatively can also be computed for a single point using `contributing_hypervolume(point)` method.


```python
for i, objectives in enumerate(moa):
    assert moa.contributing_hypervolume(objectives) == moa.contributing_hypervolumes[i]
    print("contributing hv of point", objectives, "is", moa.contributing_hypervolume(objectives))

print("All contributing hypervolumes:", moa.contributing_hypervolumes)
```

    contributing hv of point [3, 2, 0] is 2
    contributing hv of point [1, 1, 1] is 21
    All contributing hypervolumes: [Fraction(2, 1), Fraction(21, 1)]
    

### Hypervolume improvement
Returns the improvement of the hypervolume if we would add the point to the archive.


```python
point = [1, 3, 0]
print(f"hypervolume before adding {point}: {moa.hypervolume}")
print(f"hypervolume improvement of point {point}: {moa.hypervolume_improvement(point)}")
moa.add(point)
print(f"hypervolume after adding {point}: {moa.hypervolume}")
```

    hypervolume before adding [1, 3, 0]: 29
    hypervolume improvement of point [1, 3, 0]: 2
    hypervolume after adding [1, 3, 0]: 31
    

### Distance to pareto front
Returns the distance between a dominated point and the pareto front.


```python
print(f"Current archive: {list(moa)}")
print("Distance of [3, 2, 1] to pareto front:", moa.distance_to_pareto_front([3, 2, 1]))
print("Distance of [3, 2, 2] to pareto front:", moa.distance_to_pareto_front([3, 2, 2]))
```

    Current archive: [[3, 2, 0], [1, 3, 0], [1, 1, 1]]
    Distance of [3, 2, 1] to pareto front: 0.0
    Distance of [3, 2, 2] to pareto front: 1.0
    

### Turning fractions on and off
To avoid the loss of precision, fractions are used by default. Changing this to float can be done by setting function attributes `hypervolume_final_float_type` and `hypervolume_computation_float_type`.


```python
import fractions
get_mo_archive.hypervolume_computation_float_type = fractions.Fraction
get_mo_archive.hypervolume_final_float_type = fractions.Fraction

moa3_fr = get_mo_archive([[1, 2, 3], [2, 1, 3], [3, 3, 1.32], [1.3, 1.3, 3], [1.7, 1.1, 2]], reference_point=[4, 4, 4])
print(moa3_fr.hypervolume)

get_mo_archive.hypervolume_computation_float_type = float
get_mo_archive.hypervolume_final_float_type = float

moa3_nofr = get_mo_archive([[1, 2, 3], [2, 1, 3], [3, 3, 1.32], [1.3, 1.3, 3], [1.7, 1.1, 2]], reference_point=[4, 4, 4])
print(moa3_nofr.hypervolume)
```

    161245156349030777798724819133399/10141204801825835211973625643008
    15.899999999999999
    

### Additional functionalities:
MOArchive also implements additional functions to check for the given point not in the archive:
- `in_domain`: point is in domain?
- `dominates`: point is dominated by the archive?
- `dominators`: which/how many points dominate the given point?


```python
points_list = [[5, 5, 0], [2, 2, 2], [0, 2, 3]]
print("archive:", list(moa), "\n")
print("point     | in domain | dominates | num of dominators | dominators")
print("----------|-----------|-----------|-------------------|-----------")
for point in points_list:
    print(f"{point} | {moa.in_domain(point):9} | {moa.dominates(point):9} | "
          f"{moa.dominators(point, number_only=True):17} | {moa.dominators(point)}")
```

    archive: [[3, 2, 0], [1, 3, 0], [1, 1, 1]] 
    
    point     | in domain | dominates | num of dominators | dominators
    ----------|-----------|-----------|-------------------|-----------
    [5, 5, 0] |         0 |         1 |                 2 | [[3, 2, 0], [1, 3, 0]]
    [2, 2, 2] |         1 |         1 |                 1 | [[1, 1, 1]]
    [0, 2, 3] |         1 |         0 |                 0 | []
    

