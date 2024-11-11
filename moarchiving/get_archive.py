from moarchiving.moarchiving2d import BiobjectiveNondominatedSortedList as MOArchive2d
from moarchiving.moarchiving3d import MOArchive3d
from moarchiving.moarchiving4d import MOArchive4d

import warnings as _warnings
try:
    import fractions
except ImportError:
    _warnings.warn('`fractions` module not installed, arbitrary precision hypervolume computation not available')


def get_archive(list_of_f_vals=None, reference_point=None, infos=None, n_obj=None):
    """
    Factory function for creating MOArchive objects of the appropriate dimensionality.
    Args:
        list_of_f_vals: list of objective vectors, can be None if n_obj is provided
        reference_point: reference point for the archive
        infos: list of additional information for each objective vector
        n_obj: must be provided if list_of_f_vals is None

    Returns:
        MOArchive object of the appropriate dimensionality, based on the number of objectives
    """
    if not hasattr(get_archive, "hypervolume_final_float_type"):
        try:
            get_archive.hypervolume_final_float_type = fractions.Fraction
        except:
            get_archive.hypervolume_final_float_type = float
    if not hasattr(get_archive, "hypervolume_computation_float_type"):
        try:
            get_archive.hypervolume_computation_float_type = fractions.Fraction
        except:
            get_archive.hypervolume_computation_float_type = float

    assert list_of_f_vals is not None or n_obj is not None, \
        "Either list_of_f_vals or n_obj must be provided"
    if list_of_f_vals is not None and len(list_of_f_vals) > 0 and n_obj is not None:
        assert len(list_of_f_vals[0]) == n_obj, \
            "The number of objectives in list_of_f_vals must match n_obj"
    if n_obj is None:
        n_obj = len(list_of_f_vals[0])
    if reference_point is not None:
        assert len(reference_point) == n_obj, \
            "The number of objectives in reference_point must match n_obj"

    if n_obj == 2:
        return MOArchive2d(list_of_f_vals, reference_point=reference_point, infos=infos,
                           hypervolume_final_float_type=get_archive.hypervolume_final_float_type,
                           hypervolume_computation_float_type=get_archive.hypervolume_computation_float_type)
    elif n_obj == 3:
        return MOArchive3d(list_of_f_vals, reference_point=reference_point, infos=infos,
                           hypervolume_final_float_type=get_archive.hypervolume_final_float_type,
                           hypervolume_computation_float_type=get_archive.hypervolume_computation_float_type)
    elif n_obj == 4:
        return MOArchive4d(list_of_f_vals, reference_point=reference_point, infos=infos,
                           hypervolume_final_float_type=get_archive.hypervolume_final_float_type,
                           hypervolume_computation_float_type=get_archive.hypervolume_computation_float_type)
    else:
        raise ValueError(f"Unsupported number of objectives: {n_obj}")

