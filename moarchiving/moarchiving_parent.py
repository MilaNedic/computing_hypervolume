# -*- coding: utf-8 -*-

from moarchiving.moarchiving_utils import DLNode, my_lexsort, init_sentinels_new


inf = float('inf')


class MOArchiveParent:
    """ Parent class for Moarchiving 3D and 4D classes, to avoid code duplication """

    def __init__(self, list_of_f_vals=None, reference_point=None, infos=None, n_obj=None,
                 hypervolume_final_float_type=None,
                 hypervolume_computation_float_type=None):
        """ Create a new archive object.
        Args:
            list_of_f_vals: list of objective vectors
            reference_point: reference point for the hypervolume calculation
            infos: list of additional information for each objective vector, of the same length as
            list_of_f_vals
            n_obj: number of objectives
        """
        self.hypervolume_final_float_type = hypervolume_final_float_type
        self.hypervolume_computation_float_type = hypervolume_computation_float_type

        if list_of_f_vals is not None and len(list_of_f_vals):
            try:
                list_of_f_vals = list_of_f_vals.tolist()
            except:
                pass
            list_of_f_vals = [list(f_vals) for f_vals in list_of_f_vals]
            if len(list_of_f_vals[0]) != n_obj:
                raise ValueError(f"need elements of length {n_obj}, got {list_of_f_vals[0]}"
                                 " as first element")
        else:
            list_of_f_vals = []
        self.n_dim = n_obj

        if infos is None:
            infos = [None] * len(list_of_f_vals)

        if reference_point is not None:
            self.reference_point = list(reference_point)
            self.head = self.setup_cdllist(list_of_f_vals, self.reference_point, infos)
        else:
            self.reference_point = None
            self.head = self.setup_cdllist(list_of_f_vals, [inf] * self.n_dim, infos)
        self._kink_points = None

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

    def __len__(self):
        return len(self.points)

    def add(self, new, info=None, update_hypervolume=True):
        raise NotImplementedError("This method should be implemented in the child class")

    def remove(self, f_vals):
        raise NotImplementedError("This method should be implemented in the child class")

    def add_list(self, list_of_f_vals, infos=None):
        raise NotImplementedError("This method should be implemented in the child class")

    def copy(self):
        raise NotImplementedError("This method should be implemented in the child class")

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

    def in_domain(self, f_vals, reference_point=None):
        """return `True` if `f_vals` is dominating the reference point,
        `False` otherwise. `True` means that `f_vals` contributes to
        the hypervolume if not dominated by other elements.
        """

        try:
            if len(f_vals) != self.n_dim:
                raise ValueError(f"argument `f_vals` must be of length {self.n_dim}, "
                                 f"was ``{f_vals}``")
        except TypeError:
            raise TypeError(f"argument `f_vals` must be a list, was ``{f_vals}``")

        if reference_point is None:
            reference_point = self.reference_point
        if reference_point is None:
            return True

        if any(f_vals[i] >= reference_point[i] for i in range(self.n_dim)):
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
    def points(self):
        """`list` of coordinates of the non-dominated points in the archive"""
        return [point.x[:self.n_dim] for point in self._points_generator()]

    @property
    def infos(self):
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
    def hypervolume_plus(self):
        if self.reference_point is None:
            raise ValueError("to compute the hypervolume_plus a reference"
                             " point is needed (must be given initially)")
        return self._hypervolume_plus

    @property
    def contributing_hypervolumes(self):
        """`list` of hypervolume contributions of each point in the archive"""
        return [self.contributing_hypervolume(point[:self.n_dim]) for point in self.points]

    def contributing_hypervolume(self, f_vals):
        """ Returns the hypervolume contribution of a point in the archive """
        if f_vals in self.points:
            hv_before = self._hypervolume
            removed_info = self.remove(f_vals)
            hv_after = self._hypervolume
            self.add(f_vals, info=removed_info)
            return hv_before - hv_after
        else:
            return self.hypervolume_improvement(f_vals)

    def _get_kink_points(self):
        raise NotImplementedError("This method should be implemented in the child class")

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

        points = self.points

        if len(points) == 0:
            return sum([ref_di[i] ** 2 for i in range(self.n_dim)]) ** 0.5

        if self._kink_points is None:
            self._kink_points = self._get_kink_points()
        distances_squared = []

        for point in self._kink_points:
            distances_squared.append(sum([max((0, f_vals[i] - point[i])) ** 2
                                          for i in range(self.n_dim)]))
        return min(distances_squared) ** 0.5

    def distance_to_hypervolume_area(self, f_vals):
        """ Returns the distance to the hypervolume area of the archive """
        if self.reference_point is None:
            return 0
        return sum([max((0, f_vals[i] - self.reference_point[i])) ** 2
                    for i in range(self.n_dim)])**0.5

    def hypervolume_improvement(self, f_vals):
        raise NotImplementedError("This method should be implemented in the child class")

    def _set_HV(self):
        """ Set the hypervolume of the archive """
        self._hypervolume = self.hypervolume_final_float_type(self.compute_hypervolume())
        if self._hypervolume > 0:
            self._hypervolume_plus = -self._hypervolume
        return self._hypervolume

    def compute_hypervolume(self):
        raise NotImplementedError("This method should be implemented in the child class")

    def setup_cdllist(self, points, ref, infos):
        """ Set up a circular doubly linked list from the given data and reference point """
        points = [p for p in points if self.strictly_dominates(p, ref)]
        n = len(points)

        head = [DLNode(info=info) for info in ["s1", "s2", "s3"] + [None] * n]
        # init_sentinels_new accepts a list at the beginning, therefore we use head[0:3]
        init_sentinels_new(head[0:3], ref, self.n_dim)
        di = self.n_dim - 1  # Dimension index for sorting (z-axis in 3D)

        if n > 0:
            # Convert data to a structured format suitable for sorting and linking
            if self.n_dim == 3:
                # Using lexsort to sort by z, y, x in ascending order
                sorted_indices = my_lexsort(([p[0] for p in points], [p[1] for p in points],
                                             [p[2] for p in points]))
            elif self.n_dim == 4:
                # Using lexsort to sort by w, z, y, x in ascending order
                sorted_indices = my_lexsort(([p[0] for p in points], [p[1] for p in points],
                                             [p[2] for p in points], [p[3] for p in points]))
            else:
                raise ValueError("Only 3D and 4D points are supported")

            # Create nodes from sorted points
            for i, index in enumerate(sorted_indices):
                head[i + 3].x = points[index]
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
