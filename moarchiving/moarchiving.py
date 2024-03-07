"""This module contains a MOO archive class for n=3 and n=4 dimnesions
    for calculating the hypervolume.
"""

import warnings as _warnings
import bisect as _bisect
import fractions

inf = float('inf')

class moarchiving(list):
    
    def __init__(self,
             list_of_f_pairs=None,
             reference_point=None,
             sort=sorted):
        
        pass