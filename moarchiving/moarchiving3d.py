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
                     lexicographic_less, one_contribution_3d)
from moarchiving2d import BiobjectiveNondominatedSortedList as MOArchive2D
from sortedcontainers import SortedList
import numpy as np
import warnings as _warnings
from moarchiving_utils import DLNode, my_lexsort, MySortedList

del division, print_function, unicode_literals

inf = float('inf')


class MOArchive3d:
    def __init__(self, list_of_f_vals=None, reference_point=None, infos=None):
        if list_of_f_vals is not None and len(list_of_f_vals):
            try:
                list_of_f_vals = list_of_f_vals.tolist()
            except:
                pass
            self.n_dim = len(list_of_f_vals[0])
            if self.n_dim != 3:
                raise ValueError("need elements of length 3, got %s"
                                 " as first element" % str(list_of_f_vals[0]))
        else:
            self.n_dim = 3
            list_of_f_vals = []
        if infos is None:
            infos = [None] * len(list_of_f_vals)

        if reference_point is not None:
            self.reference_point = list(reference_point)
            self.head = self.setup_cdllist(list_of_f_vals, self.reference_point, infos)
        else:
            self.reference_point = None
            self.head = self.setup_cdllist(list_of_f_vals, [inf] * self.n_dim, infos)

        self.preprocessing()
        # self.print_cdllist()
        # self.print_cxcy()
        self._set_HV()

    def print_cdllist(self):
        """ For debugging purposes: print the circular doubly linked list"""
        di = self.n_dim - 1
        print("Circular Doubly-Linked List:")
        current = self.head.next[di]
        print(f"(head) {self.head.x[:self.n_dim]} <-> ", end="")
        while current is not None and current != self.head:
            print(f"{current.x[:self.n_dim]} <-> ", end="")
            current = current.next[di] if current.next[di] != self.head else None
        print("(head)")

    def print_cxcy(self):
        """ For debugging purposes: print the cx and cy values of the points in the archive"""
        di = self.n_dim - 1
        print("cx and cy values:")
        current = self.head.next[di]
        print(f"({f'{self.head.info})':6} {str(self.head.x[:self.n_dim]):22} "
              f"cx={f'({self.head.closest[0].info}),':7} "
              f"cy={f'({self.head.closest[1].info})':6}",
              f"ndomr={self.head.ndomr}")
        while current is not None and current != self.head:
            print(f"({f'{current.info})':6} {str(current.x[:self.n_dim]):22} "
                  f"cx={f'({current.closest[0].info}),':7} "
                  f"cy={f'({current.closest[1].info})':6}",
                  f"ndomr={current.ndomr}")
            current = current.next[di] if current.next[di] != self.head else None

    def add(self, new, info=None, update_hypervolume=True):
        """
        4) Data Structure Updates: Adding a new point u to the
        data structure maintained by HV3D+ requires setting attributes
        u.cx and u.cy, updating the corresponding attributes of the
        remaining points in the lexicographically sorted list Q, and
        inserting u into Q. These operations are performed in linear
        time in a single sweep of Q, as follows (cy attributes are
        updated in a similar way, but with the roles of the x- and
        y-coordinate switched).
        """

        # q is the current point (so that we are consistent with the paper),
        # stop is the head of the list, and first_iter is a flag to check if we are at the
        # first iteration (since the first and last points are the same)
        q = self.head
        stop = self.head
        first_iter = True

        # Add 0.0 for 3d points so that it matches the original C code and create a new node object
        if self.n_dim == 3:
            new = new + [0.0]
        u = DLNode(x=new, info=info)
        di = self.n_dim - 1

        # loop over all the points in the archive and save the best candidates for cx and cy,
        # and check if the new point is dominated by any of the points in the archive
        dominated = False
        best_cx_candidates = None
        best_cy_candidates = None
        inserted = False

        while q != stop or first_iter:
            first_iter = False

            # check if the new point is dominated by the current point
            if all(q.x[i] <= u.x[i] for i in range(self.n_dim)):
                dominated = True
                break
            # check if the new point dominates the current point
            if all(u.x[i] <= q.x[i] for i in range(self.n_dim)):
                q_next = q.next[di]
                remove_from_z(q)
                q = q_next
                continue

            """
            1) Set u.cx to the point q ∈ Q with the smallest q_x > u_x
            such that q_y < u_y and q <L u. If such a point is not
            unique, the alternative with the smallest q_y is preferred
            """
            if lexicographic_less(q.x, u.x) and q.x[0] > u.x[0] and q.x[1] < u.x[1]:
                if best_cx_candidates is None or q.x[0] < best_cx_candidates.x[0]:
                    best_cx_candidates = q
                elif q.x[0] == best_cx_candidates.x[0] and q.x[1] < best_cx_candidates.x[1]:
                    best_cx_candidates = q
            if lexicographic_less(q.x, u.x) and q.x[0] < u.x[0] and q.x[1] > u.x[1]:
                if best_cy_candidates is None or q.x[1] < best_cy_candidates.x[1]:
                    best_cy_candidates = q
                elif q.x[1] == best_cy_candidates.x[1] and q.x[0] < best_cy_candidates.x[0]:
                    best_cy_candidates = q

            """
            2) For q ∈ Q, set q.cx to u iff u_y < q_y and u <L q, and
            either q_x < u_x < (q.cx)_x or u_x = (q.cx)_x and u_y ≤
            (q.cx)_y.
            """
            if u.x[1] < q.x[1] and lexicographic_less(u.x, q.x):
                if (q.x[0] < u.x[0] < q.closest[0].x[0] or
                        (u.x[0] == q.closest[0].x[0] and u.x[1] <= q.closest[0].x[1])):
                    q.closest[0] = u
            if u.x[0] < q.x[0] and lexicographic_less(u.x, q.x):
                if (q.x[1] < u.x[1] < q.closest[1].x[1] or
                        (u.x[1] == q.closest[1].x[1] and u.x[0] <= q.closest[1].x[0])):
                    q.closest[1] = u
            """
            3) Insert u into Q immediately before the point q ∈ Q with
            the lexicographically smallest q such that u <L q.
            """
            # If the point is not dominated by any other point in the archive so far,
            # then it also won't be dominated by the points that come after it in the archive,
            # as the points are sorted in lexicographic order
            if lexicographic_less(u.x, q.x) and not inserted and not dominated:
                u.next[di] = q
                u.prev[di] = q.prev[di]
                q.prev[di].next[di] = u
                q.prev[di] = u
                inserted = True

            q = q.next[di]

        if not dominated:
            u.closest[0] = best_cx_candidates
            u.closest[1] = best_cy_candidates

        if update_hypervolume:
            # TODO: maybe this can be done more efficiently, by only adding hypervolume
            #  contribution of the new point
            self._set_HV()

    def remove(self, f_vals):
        """
        Removing a point u ∈ Q also requires updating the cx and
        cy attributes of the remaining points, as follows.
        1) For every p ∈ Q \ {u} such that p.cx = u, set p.cx to the
        point q ∈ Q \ {u} with the smallest qx > p_x such that
        q_y < py and q <L p (and analogously for p.cy). If such
        a point is not unique, the alternative with the smallest
        q_y (respectively, q_x) is preferred.
        """

        di = self.n_dim - 1  # Dimension index for sorting (z-axis in 3D)
        current = self.head.next[di]
        stop = self.head.prev[di]

        # Using SortedList to manage nodes by their y-coordinate, supporting custom sorting needs
        T = SortedList(key=lambda node: (node.x[1], node.x[0]))

        # Include sentinel nodes to manage edge conditions
        T.add(self.head)  # self.head is a left sentinel
        T.add(self.head.prev[di])  # right sentinel
        remove_node = None

        while current != stop:
            if current.x[:3] == f_vals:
                remove_node = current
                current = current.next[di]
                continue
            T.add(current)

            # Remove nodes dominated by the current node
            nodes_to_remove = [node for node in T if node != current and
                               self.strictly_dominates(current.x, node.x, n_dim=2)]
            for node in nodes_to_remove:
                T.remove(node)

            if current.closest[0].x[:3] == f_vals:
                # For every p ∈ Q \ {u} such that p.cx = u, set p.cx to the
                #         point q ∈ Q \ {u} with the smallest q_x > p_x such that
                #         q_y < p_y and q <L p
                current.closest[1] = current.closest[1]
                cx_candidates = [node for node in T if node.x[0] > current.x[0] and node.x[1] < current.x[1]]
                if cx_candidates:
                    current.closest[0] = min(cx_candidates, key=lambda node: node.x[0])
                else:
                    current.closest[0] = self.head

            if current.closest[1].x[:3] == f_vals:
                # For every p ∈ Q \ {u} such that p.cy = u, set p.cy to the
                #         point q ∈ Q \ {u} with the smallest q_y > p_y such that
                #         q_x < p_x and q <L p
                current.closest[1] = current.closest[1]
                cy_candidates = [node for node in T if node.x[1] > current.x[1] and node.x[0] < current.x[0]]
                if cy_candidates:
                    current.closest[1] = min(cy_candidates, key=lambda node: node.x[1])
                else:
                    current.closest[1] = self.head.prev[di]

            """
            # Adjust closest if it points to itself
            if current.closest[0] == current:
                current.closest[0] = self.head
            if current.closest[1] == current:
                current.closest[1] = self.head.prev[di]
            """
            current = current.next[di]

        if remove_node is not None:
            remove_from_z(remove_node)
        else:
            _warnings.warn(f"Point {f_vals} not found in the archive")

        T.clear()  # Clean up AVL tree after processing
        self._set_HV()

    def add_list(self, list_of_f_vals, infos=None):
        if infos is None:
            infos = [None] * len(list_of_f_vals)
        for f_val, info in zip(list_of_f_vals, infos):
            self.add(f_val, info=info, update_hypervolume=False)
        self._set_HV()

    def copy(self):
        # TODO: can probably be done more efficiently (by looping over the DLL and copying nodes)
        return MOArchive3d(self.points_list, self.reference_point, self.infos_list)

    def dominates(self, f_val):
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

    def dominators(self, f_val, number_only=False):
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

    def in_domain(self, f_pair, reference_point=None):
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

    def _points_generator(self, include_head=False):
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
    def points_list(self):
        """`list` of coordinates of the non-dominated points in the archive"""
        return [point.x[:self.n_dim] for point in self._points_generator()]

    @property
    def infos_list(self):
        """`list` of complementary information corresponding to each archive entry,
        corresponding to each of the points in the archive"""
        return [point.info for point in self._points_generator()]

    @property
    def hypervolume(self):
        if self.reference_point is None:
            raise ValueError("to compute the hypervolume a reference"
                             " point is needed (must be given initially)")
        return self._hypervolume

    @property
    def contributing_hypervolumes(self):
        return [self.contributing_hypervolume(point) for point in self._points_generator()]

    def contributing_hypervolume(self, f_vals):
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
         2D archive of all possible kink points found so far, and another 2D archive which stores
         the non-dominated points so far in the sweep """
        if self.reference_point is None:
            ref_point = [inf] * self.n_dim
        else:
            ref_point = self.reference_point

        # Add a point that will be last in the sweep, to get the last kink points
        points = self.points_list + [[0, 0, ref_point[2]]]

        # initialize the two states, one for points and another for kink points
        points_state = MOArchive2D([[ref_point[0], -inf], [-inf, ref_point[1]]])
        kink_candidates = MOArchive2D([ref_point[:2]])
        # initialize the point dictionary, which will store the third coordinate of the points
        point_dict = {
            tuple(ref_point[:2]): -inf
        }
        kink_points = []

        for point in points:
            # add the point to the kink state to get the dominated kink points, then take it out
            if kink_candidates.add(point[:2]) is not None:
                removed = kink_candidates._removed.copy()
                for removed_point in removed:
                    z = point_dict[tuple(removed_point)]
                    if z < point[2]:
                        kink_points.append([removed_point[0], removed_point[1], point[2]])
                kink_candidates._removed.clear()
                kink_candidates.remove(point[:2])

            # add the point to the point state, and get two new kink point candidates
            idx = points_state.add(point[:2])
            for i in range(2):
                p = [points_state[idx + i][0], points_state[idx - 1 + i][1]]
                point_dict[tuple(p)] = point[2]
                kink_candidates.add(p)

        return kink_points

    def distance_to_pareto_front(self, f_vals, ref_factor=1):
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
            return sum([ref_di[i]**2 for i in range(self.n_dim)])**0.5

        kink_points = self._get_kink_points()
        distances_squared = []

        for point in kink_points:
            distances_squared.append(sum([max((0, f_vals[i] - point[i]))**2
                                          for i in range(self.n_dim)]))
        return min(distances_squared)**0.5

    def distance_to_hypervolume_area(self, f_vals):
        """ Returns the distance to the hypervolume area of the archive """
        if self.reference_point is None:
            return 0
        return sum([max((0, f_vals[i] - self.reference_point[i])) ** 2
                    for i in range(self.n_dim)])**0.5

    def hypervolume_improvement(self, f_vals):
        """ Returns the hypervolume improvement of adding a point to the archive """
        if f_vals in self.points_list:
            return 0
        if self.dominates(f_vals):
            return -1 * self.distance_to_pareto_front(f_vals)

        return one_contribution_3d(self.head, DLNode(x=f_vals))

    def _set_HV(self):
        """ Set the hypervolume of the archive """
        self._hypervolume = self.compute_hypervolume()
        return self._hypervolume

    def compute_hypervolume(self):
        """ Compute the hypervolume of the current state of archive """
        p = self.head
        area = 0
        volume = 0

        restart_list_y(self.head)
        p = p.next[2].next[2]
        stop = self.head.prev[2]

        while p != stop:
            if p.ndomr < 1:
                p.cnext[0] = p.closest[0]
                p.cnext[1] = p.closest[1]

                area += compute_area_simple(p.x, 1, p.cnext[0], p.cnext[0].cnext[1])

                p.cnext[0].cnext[1] = p
                p.cnext[1].cnext[0] = p
            else:
                remove_from_z(p)

            volume += area * (p.next[2].x[2] - p.x[2])
            p = p.next[2]

        return volume

    def setup_cdllist(self, data, ref, infos):
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

    def preprocessing(self):
        """ Preprocessing step to determine the closest points in x and y directions,
        as described in the paper and implemented in the original C code. """
        di = self.n_dim - 1
        t = MySortedList(iterable=[self.head, self.head.next[di]],
                         key=lambda node: (node.x[1], node.x[0]))

        p = self.head.next[di].next[di]
        stop = self.head.prev[di]

        while p != stop:
            s = t.outer_delimiter_x(p)
            if self.weakly_dominates(s.x, p.x):
                p.ndomr = 1
                p = p.next[di]
                continue

            t.remove_dominated_y(p, s)
            p.closest[0] = s
            p.closest[1] = t.next_y(s)
            t.add_y(p, s)
            p = p.next[di]

        t.clear()

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

    # OLD IMPLEMENTATIONS, NOT USED IN THE CURRENT CODE
    def hypervolume_improvement_naive(self, f_vals):
        """ Returns the hypervolume improvement of adding a point to the archive """
        if f_vals in self.points_list:
            return 0
        if self.dominates(f_vals):
            return -1 * self.distance_to_pareto_front(f_vals)

        moa_copy = self.copy()
        moa_copy.add(f_vals)
        return moa_copy.hypervolume - self.hypervolume

    def _get_kink_points_tea(self):
        """ Function that returns the kink points of the archive, as described in Tea's PhD"""
        def _is_redundant(vector, existing_points):
            if len(existing_points) == 0:
                return False

            for second in existing_points:
                if _collinear(vector, second) or self.weakly_dominates(vector, second):
                    return True
            return False

        def _collinear(p1, p2, tolerance=1e-9):
            return sum(abs(p1[i] - p2[i]) < tolerance for i in range(self.n_dim)) >= 2

        points_set = self.points_list
        result = [self.reference_point]

        for a in points_set:
            candidates = [b for b in result if self.strictly_dominates(a, b)]
            for b in candidates:
                result.remove(b)

                for k in range(3):
                    v = b.copy()
                    v[k] = a[k]
                    if not _is_redundant(v, result):
                        result.append(v)
        return result

    def preprocessing_old(self):
        """ Preprocessing step to determine the closest points in x and y directions,
        as described in the paper and implemented in the original C code. """
        di = self.n_dim - 1  # Dimension index for sorting (z-axis in 3D)
        current = self.head.next[di]
        stop = self.head.prev[di]

        # Using SortedList to manage nodes by their y-coordinate, supporting custom sorting needs
        avl_tree = SortedList(key=lambda node: (node.x[1], node.x[0]))

        # Include sentinel nodes to manage edge conditions
        avl_tree.add(self.head)  # self.head is a left sentinel
        avl_tree.add(self.head.prev[di])  # right sentinel

        while current != stop:
            avl_tree.add(current)
            index = avl_tree.index(current)

            # Check if current node is dominated by any previous node in avl_tree
            dominated = False
            for node in avl_tree:
                if node != current and all(node.x[i] <= current.x[i] for i in range(3)) and any(
                        node.x[i] < current.x[i] for i in range(3)):
                    dominated = True
                    break

            if dominated:
                current.ndomr = 1
                avl_tree.remove(current)
            else:
                # Remove nodes dominated by the current node
                nodes_to_remove = [node for node in avl_tree if node != current and all(
                    current.x[i] <= node.x[i] for i in range(3)) and any(
                    current.x[i] < node.x[i] for i in range(3))]
                for node in nodes_to_remove:
                    avl_tree.remove(node)
                    node.ndomr = 1

            # Determine closest[0]: smallest q such that q_x > p_x and q_y < p_y
            x_candidates = [node for node in avl_tree if
                            node.x[0] > current.x[0] and node.x[1] < current.x[1]]
            if x_candidates:
                current.closest[0] = min(x_candidates, key=lambda node: node.x[0])
            else:
                current.closest[0] = self.head  # Fallback to sentinel if no valid candidate

            # Determine closest[1]: smallest q such that q_x < p_x and q_y > p_y
            y_candidates = [node for node in avl_tree if
                            node.x[0] < current.x[0] and node.x[1] > current.x[1]]
            if y_candidates:
                current.closest[1] = min(y_candidates, key=lambda node: node.x[1])
            else:
                current.closest[1] = self.head.prev[di]  # Fallback to sentinel if no valid candidate

            # Adjust closest if it points to itself
            if current.closest[0] == current:
                current.closest[0] = self.head
            if current.closest[1] == current:
                current.closest[1] = self.head.prev[di]

            current = current.next[di]

        avl_tree.clear()  # Clean up AVL tree after processing
