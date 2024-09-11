# -*- coding: utf-8 -*-
"""This module contains, for the time being, a single MOO archive class.

A bi-objective nondominated archive as sorted list with incremental
update in logarithmic time.

"""
from __future__ import division, print_function, unicode_literals
__author__ = "Nikolaus Hansen"
__license__ = "BSD 3-clause"
__version__ = "0.6.0"

from hv_plus import (compute_area_simple, init_sentinels_new, remove_from_z, restart_list_y,
                     lexicographic_less_4d, one_contribution_3d, hv4dplusR)
from moarchiving2d import BiobjectiveNondominatedSortedList as MOArchive2D
from moarchiving3d import MOArchive3d
from moarchiving_utils import DLNode, my_lexsort
from sortedcontainers import SortedList
import numpy as np
import warnings as _warnings

del division, print_function, unicode_literals

inf = float('inf')


class MOArchive4d:
    def __init__(self, list_of_f_vals=None, reference_point=None, infos=None):
        if list_of_f_vals is not None and len(list_of_f_vals):
            try:
                list_of_f_vals = list_of_f_vals.tolist()
            except:
                pass
            self.n_dim = len(list_of_f_vals[0])
            if self.n_dim != 4:
                raise ValueError("need elements of length 4, got %s"
                                 " as first element" % str(list_of_f_vals[0]))
        else:
            self.n_dim = 4
            list_of_f_vals = []
        if infos is None:
            infos = [None] * len(list_of_f_vals)

        if reference_point is not None:
            self.reference_point = list(reference_point)
            self.head = self.setup_cdllist(list_of_f_vals, self.reference_point, infos)
        else:
            self.reference_point = None
            self.head = self.setup_cdllist(list_of_f_vals, [inf] * self.n_dim, infos)

        self.remove_dominated()
        self._set_HV()

    def print_cdllist(self):
        """ For debugging purposes: print the circular doubly linked list"""
        di = self.n_dim - 1
        print("Circular Doubly-Linked List:")
        current = self.head.next[di]
        print(f"(head) {self.head.x[:self.n_dim]} <-> ", end="")
        while current is not None and current != self.head:
            print(f"{current.x[:self.n_dim]} (dom: {current.ndomr}) <-> ", end="")
            current = current.next[di] if current.next[di] != self.head else None
        print("(head)")

    def print_cxcy(self):
        """ For debugging purposes: print the cx and cy values of the points in the archive"""
        di = self.n_dim - 1
        print("cx and cy values:")
        current = self.head.next[di]
        print(f"({self.head.info + ')':4} {str(self.head.x[:self.n_dim]):22} "
              f"cx={'(' + self.head.closest[0].info + ')':4}, "
              f"cy={'(' + self.head.closest[1].info + ')':4}, "
              f"ndomr={self.head.ndomr}")
        while current is not None and current != self.head:
            print(f"({current.info + ')':4} {str(current.x[:self.n_dim]):22} "
                  f"cx={'(' + current.closest[0].info + ')':4}, "
                  f"cy={'(' + current.closest[1].info + ')':4}, "
                  f"ndomr={current.ndomr}")
            current = current.next[di] if current.next[di] != self.head else None

    def add(self, new, info=None, update_hypervolume=True):
        if len(new) != self.n_dim:
            raise ValueError(f"argument `f_pair` must be of length {self.n_dim}, was ``{new}``")

        if self.dominates(new) or not self.in_domain(new):
            return False

        self.__init__(self.points_list + [new], self.reference_point, self.infos_list + [info])

    def remove(self, f_vals):
        points_list = self.points_list
        if f_vals not in points_list:
            return False
        self.__init__([p for p in points_list if p != f_vals], self.reference_point,
                      [info for p, info in zip(points_list, self.infos_list) if p != f_vals])

    def add_list(self, list_of_f_vals, infos=None):
        if infos is None:
            infos = [None] * len(list_of_f_vals)
        for f_val, info in zip(list_of_f_vals, infos):
            self.add(f_val, info=info)

    def copy(self):  # SAME AS IN 3D
        # TODO: can probably be done more efficiently (by looping over the DLL and copying nodes)
        return MOArchive4d(self.points_list, self.reference_point, self.infos_list)

    def dominates(self, f_val):  # SAME AS IN 3D
        """ return `True` if any element of `points` dominates or is equal to `f_val`.
        Otherwise return `False`.
        """
        for point in self._points_generator():
            if self.weakly_dominates(point.x, f_val):
                return True
            # points are sorted in lexicographic order, so we can return False
            # once we find a point that is lexicographically greater than f_val
            elif f_val[self.n_dim - 1] < point.x[self.n_dim - 1]:
                return False
        return False

    def dominators(self, f_val, number_only=False):  # SAME AS IN 3D
        """return the list of all `f_val`-dominating elements in `self`,
        including an equal element. ``len(....dominators(...))`` is
        hence the number of dominating elements which can also be obtained
        without creating the list with ``number_only=True``.
        """
        dominators = [] if not number_only else 0
        for point in self._points_generator():
            if all(point.x[i] <= f_val[i] for i in range(self.n_dim)):
                if number_only:
                    dominators += 1
                else:
                    dominators.append(point.x[:self.n_dim])
            # points are sorted in lexicographic order, so we can break the loop
            # once we find a point that is lexicographically greater than f_val
            elif f_val[self.n_dim - 1] < point.x[self.n_dim - 1]:
                break
        return dominators

    def in_domain(self, f_pair, reference_point=None):  # SAME AS IN 3D
        """return `True` if `f_pair` is dominating the reference point,
        `False` otherwise. `True` means that `f_pair` contributes to
        the hypervolume if not dominated by other elements.

        TODO: in Nikos' code, f_pair can also be an index, not just a list of values,
        TODO: this is not implemented here (due to not having a state in form of a list of points)
        """

        if reference_point is None:
            reference_point = self.reference_point
        if reference_point is None:
            return True

        if any(f_pair[i] >= reference_point[i] for i in range(self.n_dim)):
            return False
        return True

    def _points_generator(self, include_head=False):  # SAME AS IN 3D
        """ returns the points in the archive in a form of a python generator
        instead of a circular doubly linked list """
        first_iter = True
        di = self.n_dim - 1
        if include_head:
            curr = self.head
            stop = self.head
        else:
            curr = self.head.next[di].next[di]
            stop = self.head.prev[di]
            if curr == stop:
                return
        while curr != stop or first_iter:
            yield curr
            first_iter = False
            curr = curr.next[di]

    @property
    def points_list(self):  # SAME AS IN 3D
        """`list` of coordinates of the non-dominated points in the archive"""
        return [point.x[:self.n_dim] for point in self._points_generator()]

    @property
    def infos_list(self):  # SAME AS IN 3D
        """`list` of complementary information corresponding to each archive entry,
        corresponding to each of the points in the archive"""
        return [point.info for point in self._points_generator()]

    @property
    def hypervolume(self):  # SAME AS IN 3D
        if self.reference_point is None:
            raise ValueError("to compute the hypervolume a reference"
                             " point is needed (must be given initially)")
        return self._hypervolume

    @property
    def contributing_hypervolumes(self):  # SAME AS IN 3D
        return [self.contributing_hypervolume(point) for point in self._points_generator()]

    def contributing_hypervolume(self, f_vals):  # SAME AS IN 3D
        # TODO: implement actual hypervolume contribution calculation
        if f_vals in self.points_list:
            hv_before = self._hypervolume
            self.remove(f_vals)
            hv_after = self._hypervolume
            self.add(f_vals)
            return hv_before - hv_after
        else:
            return self.hypervolume_improvement(f_vals)

    def _get_kink_points(self):
        """ Function that returns the kink points of the archive.
         Kink point are calculated by making a sweep of the archive, where the state is one
         3D archive of all possible kink points found so far, and another 3D archive which stores
         the non-dominated points so far in the sweep """
        if self.reference_point is None:
            almost_inf = 1e10  # TODO: this is a hack, should be replaced by a better solution
            ref_point = [almost_inf] * self.n_dim
        else:
            ref_point = self.reference_point

        # initialize the two states, one for points and another for kink points
        points_state = MOArchive3d(reference_point=ref_point[:3])
        kink_candidates = MOArchive3d([ref_point[:3]])
        # initialize the point dictionary, which will store the fourth coordinate of the points
        point_dict = {
            tuple(ref_point[:3]): -inf
        }
        kink_points = []

        for point in self.points_list:
            # add the point to the kink state to get the dominated kink points, then take it out
            if kink_candidates.add(point[:3]):
                removed = kink_candidates._removed.copy()
                for removed_point in removed:
                    w = point_dict[tuple(removed_point)]
                    if w < point[3]:
                        kink_points.append([removed_point[0], removed_point[1], removed_point[2],
                                            point[3]])
                kink_candidates._removed.clear()
                kink_candidates.remove(point[:3])

            # add the point to the point state, and get two new kink point candidates
            points_state.add(point[:3])
            new_kink_candidates = points_state._get_kink_points()
            new_kink_candidates = [p for p in new_kink_candidates if
                                   (p[0] == point[0] or p[1] == point[1] or p[2] == point[2])]
            for p in new_kink_candidates:
                point_dict[tuple(p)] = point[3]
                kink_candidates.add(p)

        for point in kink_candidates.points_list:
            kink_points.append([point[0], point[1], point[2], ref_point[3]])

        return kink_points

    def distance_to_pareto_front(self, f_vals, ref_factor=1):  # SAME AS IN 3D
        """ Returns the distance to the Pareto front of the archive,
        by calculating the distances to the kink points """
        if self.in_domain(f_vals) and not self.dominates(f_vals):
            return 0  # return minimum distance

        if self.reference_point is not None:
            ref_di = [ref_factor * max((0, f_vals[i] - self.reference_point[i]))
                      for i in range(self.n_dim)]
        else:
            ref_di = [0] * self.n_dim

        points = self.points_list

        if len(points) == 0:
            return sum([ref_di[i] ** 2 for i in range(self.n_dim)]) ** 0.5

        kink_points = self._get_kink_points()
        distances_squared = []

        for point in kink_points:
            distances_squared.append(sum([max((0, f_vals[i] - point[i])) ** 2
                                          for i in range(self.n_dim)]))
        return min(distances_squared) ** 0.5

    def distance_to_hypervolume_area(self, f_vals):  # SAME AS IN 3D
        """ Returns the distance to the hypervolume area of the archive """
        if self.reference_point is None:
            return 0
        return sum([max((0, f_vals[i] - self.reference_point[i])) ** 2
                    for i in range(self.n_dim)])**0.5

    def hypervolume_improvement(self, f_vals):
        raise NotImplementedError()

    def hypervolume_improvement_naive(self, f_vals):  # SAME AS IN 3D
        """ Returns the hypervolume improvement of adding a point to the archive """
        if f_vals in self.points_list:
            return 0
        if self.dominates(f_vals):
            return -1 * self.distance_to_pareto_front(f_vals)

        moa_copy = self.copy()
        moa_copy.add(f_vals)
        return moa_copy.hypervolume - self.hypervolume

    def _set_HV(self):  # SAME AS IN 3D
        """ Set the hypervolume of the archive """
        self._hypervolume = self.compute_hypervolume()
        return self._hypervolume

    def compute_hypervolume(self):
        return hv4dplusR(self.head)

    def setup_cdllist(self, data, ref, infos):  # SAME AS IN 3D
        """ Set up a circular doubly linked list from the given data and reference point """
        n = len(data)
        head = [DLNode(info=info) for info in ["s1", "s2", "s3"] + [None] * n]
        # init_sentinels_new accepts a list at the beginning, therefore we use head[0:3]
        init_sentinels_new(head[0:3], ref, self.n_dim)
        di = self.n_dim - 1  # Dimension index for sorting (z-axis in 3D)

        points = np.array(data)

        if n > 0:
            # Convert data to a structured format suitable for sorting and linking
            if self.n_dim == 3:
                # Using lexsort to sort by z, y, x in ascending order
                sorted_indices = my_lexsort((points[:, 0], points[:, 1], points[:, 2]))
            elif self.n_dim == 4:
                # Using lexsort to sort by w, z, y, x in ascending order
                sorted_indices = my_lexsort(
                    (points[:, 0], points[:, 1], points[:, 2], points[:, 3]))
            else:
                raise ValueError("Only 3D and 4D points are supported")

            # Create nodes from sorted points
            for i, index in enumerate(sorted_indices):
                head[i + 3].x = points[index].tolist()
                head[i + 3].info = infos[index]
                if self.n_dim == 3:
                    # Add 0.0 for 3d points so that it matches the original C code
                    head[i + 3].x.append(0.0)

            # Link nodes
            s = head[0].next[di]
            s.next[di] = head[3]
            head[3].prev[di] = s

            for i in range(3, n + 2):
                head[i].next[di] = head[i + 1] if i + 1 < len(head) else head[0]
                head[i + 1].prev[di] = head[i]

            s = head[0].prev[di]
            s.prev[di] = head[n + 2]
            head[n + 2].next[di] = s

        return head[0]

    def weakly_dominates(self, a, b, n_dim=None):
        """ Return True if a weakly dominates b, False otherwise """
        if n_dim is None:
            n_dim = self.n_dim
        return all(a[i] <= b[i] for i in range(n_dim))

    def strictly_dominates(self, a, b, n_dim=None):
        """ Return True if a strictly dominates b, False otherwise """
        if n_dim is None:
            n_dim = self.n_dim
        return (all(a[i] <= b[i] for i in range(n_dim)) and
                any(a[i] < b[i] for i in range(n_dim)))

    def remove_dominated(self):
        """ Preprocessing step to remove dominated points. """
        di = self.n_dim - 1  # Dimension index for sorting (z-axis in 3D)
        current = self.head.next[di]
        stop = self.head.prev[di]

        # Using SortedList to manage nodes by their y-coordinate, supporting custom sorting needs
        non_dominated_points = []
        dominated_points = []

        while current != stop:
            # Check if current node is dominated by any previous node in avl_tree
            dominated = False
            for node in non_dominated_points:
                if node != current and all(node.x[i] <= current.x[i] for i in range(3)) and any(
                        node.x[i] < current.x[i] for i in range(3)):
                    dominated = True
                    break
            if dominated:
                dominated_points.append(current)
            else:
                non_dominated_points.append(current)
            current = current.next[di]

        for point in dominated_points:
            self.remove_from_z(point)

    def remove_from_z(self, old):
        di = self.n_dim - 1
        old.prev[di].next[di] = old.next[di]
        old.next[di].prev[di] = old.prev[di]
