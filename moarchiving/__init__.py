# -*- coding: utf-8 -*-
"""This module contains, for the time being, a single MOO archive class.

A bi-objective nondominated archive as sorted list with incremental update
in logarithmic time, providing computations of overall hypervolume,
contributing hypervolumes and uncrowded hypervolume improvements.

:Author: Nikolaus Hansen, 2018

:License: BSD 3-Clause, see LICENSE file.

"""

from .moarchiving2d import BiobjectiveNondominatedSortedList
from .moarchiving3d import MOArchive3d
from .moarchiving4d import MOArchive4d
from .moarchiving_parent import MOArchiveParent
from .constrained_moarchive import CMOArchive
from moarchiving.tests import (test_moarchiving2d, test_moarchiving3d, test_moarchiving4d,
                               test_constrained_moarchiving, test_sorted_list)
from .moarchiving2d import __author__, __license__, __version__
