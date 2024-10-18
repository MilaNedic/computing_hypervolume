# -*- coding: utf-8 -*-
from moarchiving2d import BiobjectiveNondominatedSortedList as MOArchive2D
from moarchiving_utils import (DLNode, MySortedList, compute_area_simple, remove_from_z,
                               restart_list_y, lexicographic_less, one_contribution_3d)
from moarchiving_parent import MOArchiveParent

import warnings as _warnings
from sortedcontainers import SortedList

inf = float('inf')


class MOArchive3d(MOArchiveParent):
    def __init__(self, list_of_f_vals=None, reference_point=None, infos=None):
        """Create a new 3D archive. """
        super().__init__(list_of_f_vals, reference_point, infos, 3)

        self._removed = []
        self.preprocessing()
        self._set_HV()

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
        if len(new) != self.n_dim:
            raise ValueError(f"argument `f_pair` must be of length {self.n_dim}, was ``{new}``")

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
        removed = []

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
                removed.append(q.x[:3])
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

        self._removed = removed
        self._kink_points = None

        if update_hypervolume and not dominated:
            self._set_HV()

        return not dominated

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

            current = current.next[di]

        if remove_node is not None:
            remove_from_z(remove_node)
        else:
            _warnings.warn(f"Point {f_vals} not found in the archive")

        T.clear()  # Clean up AVL tree after processing
        self._kink_points = None
        self._set_HV()

    def add_list(self, list_of_f_vals, infos=None):
        if infos is None:
            infos = [None] * len(list_of_f_vals)
        for f_val, info in zip(list_of_f_vals, infos):
            self.add(f_val, info=info, update_hypervolume=False)
        self._set_HV()

    def copy(self):
        return MOArchive3d(self.points_list, self.reference_point, self.infos_list)

    def _get_kink_points(self):
        """ Function that returns the kink points of the archive.
         Kink point are calculated by making a sweep of the archive, where the state is one
         2D archive of all possible kink points found so far, and another 2D archive which stores
         the non-dominated points so far in the sweep """
        if self.reference_point is None:
            ref_point = [inf] * self.n_dim
        else:
            ref_point = self.reference_point

        # initialize the two states, one for points and another for kink points
        points_state = MOArchive2D([[ref_point[0], -inf], [-inf, ref_point[1]]])
        kink_candidates = MOArchive2D([ref_point[:2]])
        # initialize the point dictionary, which will store the third coordinate of the points
        point_dict = {
            tuple(ref_point[:2]): -inf
        }
        kink_points = []

        for point in self.points_list:
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

        # add all the remaining kink points to the list
        for point in kink_candidates:
            kink_points.append([point[0], point[1], ref_point[2]])

        return kink_points

    def hypervolume_improvement(self, f_vals):
        """ Returns the hypervolume improvement of adding a point to the archive """
        if f_vals in self.points_list:
            return 0
        if self.dominates(f_vals):
            return -1 * self.distance_to_pareto_front(f_vals)

        return one_contribution_3d(self.head, DLNode(x=f_vals))

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
