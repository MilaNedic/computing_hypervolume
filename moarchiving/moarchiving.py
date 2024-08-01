# -*- coding: utf-8 -*-
"""This module contains, for the time being, a single MOO archive class.

A bi-objective nondominated archive as sorted list with incremental
update in logarithmic time.

"""
from __future__ import division, print_function, unicode_literals
__author__ = "Nikolaus Hansen"
__license__ = "BSD 3-clause"
__version__ = "0.6.0"

import copy
from hv_plus import (compute_area_simple, init_sentinels_new, remove_from_z, restart_list_y,
                     lexicographic_less)
from sortedcontainers import SortedList
import numpy as np

del division, print_function, unicode_literals



inf = float('inf')


class DLNode:
    def __init__(self, x=None, info=None):
        self.x = x if x else [None, None, None, None]
        self.closest = [None, None]  # closest in x coordinate, closest in y coordinate
        self.cnext = [None, None]  # current next
        self.next = [None, None, None, None]
        self.prev = [None, None, None, None]
        self.ndomr = 0  # number of dominators
        self.info = info


class MOArchive:
    def __init__(self, list_of_f_vals=None, reference_point=None, infos=None):
        if list_of_f_vals is not None and len(list_of_f_vals):
            try:
                list_of_f_vals = list_of_f_vals.tolist()
            except:
                pass
            self.n_dim = len(list_of_f_vals[0])
            if self.n_dim < 3 or self.n_dim > 4:
                raise ValueError("need elements of len 3 or 4, got %s"
                                 " as first element" % str(list_of_f_vals[0]))
        else:
            self.n_dim = 3  # TODO: how to deal with this?
        if infos is None:
            infos = [None] * len(list_of_f_vals)

        if reference_point is not None:
            self.reference_point = list(reference_point)
            self.head = self.setup_cdllist(list_of_f_vals, self.reference_point, infos)
        else:
            self.reference_point = None
            self.head = self.setup_cdllist(list_of_f_vals, [inf] * self.n_dim, infos)

        self.preprocessing()
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
        print(f"({self.head.info + ')':4} {str(self.head.x[:self.n_dim]):22} "
              f"cx={'(' + self.head.closest[0].info + ')':4}, "
              f"cy={'(' + self.head.closest[1].info + ')':4}",
              f"ndomr={self.head.ndomr}")
        while current is not None and current != self.head:
            print(f"({current.info + ')':4} {str(current.x[:self.n_dim]):22} "
                  f"cx={'(' + current.closest[0].info + ')':4}, "
                  f"cy={'(' + current.closest[1].info + ')':4}",
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
                q_next = q.next[self.n_dim - 1]
                remove_from_z(q)
                q = q_next
                continue
                # q.ndomr += 1

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

            q = q.next[self.n_dim - 1]

        if not dominated:
            u.closest[0] = best_cx_candidates
            u.closest[1] = best_cy_candidates

        if update_hypervolume:
            # TODO: maybe this can be done more efficiently, by only adding hypervolume
            #  contribution of the new point
            self._set_HV()

    def remove(self, f_pair):
        raise NotImplementedError()

    def add_list(self, list_of_f_vals, infos=None):
        if infos is None:
            infos = [None] * len(list_of_f_vals)
        for f_val, info in zip(list_of_f_vals, infos):
            self.add(f_val, info=info, update_hypervolume=False)
        self._set_HV()

    def copy(self):
        raise NotImplementedError()

    def bisect_left(self, f_pair, lowest_index=0):
        raise NotImplementedError()

    def dominates(self, f_pair):
        raise NotImplementedError()

    def dominates_with(self, idx, f_pair):
        raise NotImplementedError()

    def dominators(self, f_pair, number_only=False):
        raise NotImplementedError()

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

    def cdllist_to_list(self):
        """ returns the points in the archive in a form of a python list
        instead of a circular doubly linked list """
        points = []
        curr = self.head.next[self.n_dim - 1].next[self.n_dim - 1]
        stop = self.head.prev[self.n_dim - 1]
        while curr != stop:
            points.append(curr)
            curr = curr.next[self.n_dim - 1]
        return points

    @property
    def points(self):
        """`list` of coordinates of the non-dominated points in the archive"""
        return [point.x[:self.n_dim] for point in self.cdllist_to_list()]

    @property
    def infos(self):
        """`list` of complementary information corresponding to each archive entry,
        corresponding to each of the points in the archive"""
        return [point.info for point in self.cdllist_to_list()]

    @property
    def hypervolume(self):
        if self.reference_point is None:
            raise ValueError("to compute the hypervolume a reference"
                             " point is needed (must be given initially)")
        return self._hypervolume

    @property
    def contributing_hypervolumes(self):
        return [self.contributing_hypervolume(point) for point in self.cdllist_to_list()]

    def contributing_hypervolume(self, f_pair):
        raise NotImplementedError()

    def distance_to_pareto_front(self, f_pair, ref_factor=1):
        raise NotImplementedError()

    def distance_to_hypervolume_area(self, f_pair):
        raise NotImplementedError()

    def hypervolume_improvement(self, f_pair):
        raise NotImplementedError()

    def _set_HV(self):
        if self.reference_point is None:
            return None
        self._hypervolume = self.compute_hypervolume(self.reference_point)
        return self._hypervolume

    def compute_hypervolume(self, reference_point):
        if reference_point is None:
            raise ValueError("to compute the hypervolume a reference"
                             " point is needed (was `None`)")
        p = self.head
        area = 0
        volume = 0

        # TODO: figure out why this three lines break the code (just changing self.head to p)
        # restart_list_y(p)
        # p = p.next[2].next[2]
        # stop = p.prev[2]

        restart_list_y(self.head)
        p = p.next[2].next[2]
        stop = self.head.prev[2]

        while p != stop:
            if p.ndomr < 1:
                p.cnext[0] = p.closest[0]
                p.cnext[1] = p.closest[1]

                if len(self.infos) < 80:
                    pass

                area += compute_area_simple(p.x, 1, p.cnext[0], p.cnext[0].cnext[1])

                p.cnext[0].cnext[1] = p
                p.cnext[1].cnext[0] = p
            else:
                remove_from_z(p)

            volume += area * (p.next[2].x[2] - p.x[2])
            p = p.next[2]

        return volume

    def _subtract_HV(self, idx0, idx1=None):
        raise NotImplementedError()

    def _add_HV(self, idx):
        raise NotImplementedError()

    def setup_cdllist(self, data, ref, infos):
        n = len(data)
        head = [DLNode(info=info) for info in ["s1", "s2", "s3"] + [None] * n]
        # init_sentinels_new accepts a list at the beginning, therefore we use head[0:3]
        init_sentinels_new(head[0:3], ref, self.n_dim)
        di = self.n_dim - 1  # Dimension index for sorting (z-axis in 3D)

        points = np.array(data)

        if n > 0:
            # Convert data to a structured format suitable for sorting and linking
            if self.n_dim == 3:
                # Using np.lexsort to sort by z, y, x in ascending order
                sorted_indices = np.lexsort((points[:, 0], points[:, 1], points[:, 2]))
            elif self.n_dim == 4:
                # Using np.lexsort to sort by w, z, y, x in ascending order
                sorted_indices = np.lexsort(
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

    @property
    def discarded(self):
        raise NotImplementedError()

    @staticmethod
    def _random_archive(max_size=500, p_ref_point=0.5):
        raise NotImplementedError()

    def _asserts(self):
        raise NotImplementedError()


if __name__ == "__main__":
    import doctest
    print('doctest.testmod() in moarchiving.py')
    print(doctest.testmod())
