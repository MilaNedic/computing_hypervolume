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
from hv_plus import compute_area_simple, init_sentinels_new, remove_from_z, restart_list_y
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

    def add(self, f_pair, info=None):
        raise NotImplementedError()

    def _add_at(self, idx, f_pair, info=None):
        raise NotImplementedError()

    def remove(self, f_pair):
        raise NotImplementedError()

    def add_list(self, list_of_f_pairs):
        raise NotImplementedError()

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
        """`list` of coordinates of the nondominated points in the archive"""
        return [point.x for point in self.cdllist_to_list()]

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
