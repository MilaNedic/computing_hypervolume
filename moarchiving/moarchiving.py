"""This module contains a MOO archive class for n=3 and n=4 dimnesions
    for calculating the hypervolume.
"""

import warnings as _warnings
import bisect as _bisect
import fractions

inf = float('inf')

class moarchiving(list):
    
    def __init__(self,
             list_of_f_triplets=None,
             reference_point=None,
             sort=sorted):
        
        pass
    
    def dominates_with(self, idx, f_triplet):
        
        """return 'True' if 'self[idx]' dominates or is equal to 'f_triplet'.
        Otherwise return 'False' or 'None' if 'idx' is out-of-range.
        """
        
        if idx < 0 or idx >= len(self):
            return None
        if self[idx][0] <= f_triplet[0] and self[idx][1] <= f_triplet[1] and self[idx][2] <= f_triplet[2]: # we have to check three cooridnates in 3-D and four coordinates in 4-D
            return True
        return False