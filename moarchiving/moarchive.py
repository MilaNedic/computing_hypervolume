from moarchiving2d import BiobjectiveNondominatedSortedList as MOArchive2d
from moarchiving3d import MOArchive3d
from moarchiving4d import MOArchive4d


def MOArchive(list_of_f_vals=None, reference_point=None, infos=None, n_obj=None):
    assert list_of_f_vals is not None or n_obj is not None, \
        "Either list_of_f_vals or n_obj must be provided"
    if list_of_f_vals is not None and len(list_of_f_vals) > 0 and n_obj is not None:
        assert len(list_of_f_vals[0]) == n_obj, \
            "The number of objectives in list_of_f_vals must match n_obj"
    if n_obj is None:
        n_obj = len(list_of_f_vals[0])

    if n_obj == 2:
        return MOArchive2d(list_of_f_vals, reference_point)
    elif n_obj == 3:
        return MOArchive3d(list_of_f_vals, reference_point, infos)
    elif n_obj == 4:
        return MOArchive4d(list_of_f_vals, reference_point, infos)
    else:
        raise ValueError(f"Unsupported number of objectives: {n_obj}")

