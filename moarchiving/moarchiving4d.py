# -*- coding: utf-8 -*-
from hv_plus import hv4dplusR
from moarchiving3d import MOArchive3d
from moarchiving_parent import MOArchiveParent

inf = float('inf')


class MOArchive4d(MOArchiveParent):
    def __init__(self, list_of_f_vals=None, reference_point=None, infos=None):
        super().__init__(list_of_f_vals, reference_point, infos, 4)

        self._hypervolume_already_computed = False
        self.remove_dominated()
        self._set_HV()

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

        self.__init__(self.points_list + list_of_f_vals, self.reference_point, self.infos_list + infos)

    def copy(self):
        return MOArchive4d(self.points_list, self.reference_point, self.infos_list)

    def _get_kink_points(self):
        """ Function that returns the kink points of the archive.
         Kink point are calculated by making a sweep of the archive, where the state is one
         3D archive of all possible kink points found so far, and another 3D archive which stores
         the non-dominated points so far in the sweep """
        if self.reference_point is None:
            almost_inf = 1e10  # TODO: this is a hack, but I don't find a better way to do it...
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

    def hypervolume_improvement(self, f_vals):
        return self.hypervolume_improvement_naive(f_vals)

    def hypervolume_improvement_naive(self, f_vals):
        """ Returns the hypervolume improvement of adding a point to the archive """
        if f_vals in self.points_list:
            return 0
        if self.dominates(f_vals):
            return -1 * self.distance_to_pareto_front(f_vals)

        moa_copy = self.copy()
        moa_copy.add(f_vals)
        return moa_copy.hypervolume - self.hypervolume

    def compute_hypervolume(self):
        if self._hypervolume_already_computed:
            return self._hypervolume
        return hv4dplusR(self.head)

    def remove_dominated(self):
        """ Preprocessing step to remove dominated points. """
        di = self.n_dim - 1
        current = self.head.next[di]
        stop = self.head.prev[di]

        non_dominated_points = []
        dominated_points = []

        while current != stop:
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
