from sortedcontainers import SortedKeyList


class DLNode:
    def __init__(self, x=None, info=None):
        self.x = x if x else [None, None, None, None]
        self.closest = [None, None]  # closest in x coordinate, closest in y coordinate
        self.cnext = [None, None]  # current next
        self.next = [None, None, None, None]
        self.prev = [None, None, None, None]
        self.ndomr = 0  # number of dominators
        self.info = info

    def copy(self):
        new_node = DLNode()
        for var in self.__dict__:
            if isinstance(getattr(self, var), list):
                setattr(new_node, var, getattr(self, var).copy())
            else:
                setattr(new_node, var, getattr(self, var))
        return new_node


class MySortedList(SortedKeyList):
    def __init__(self, iterable=None, key=lambda node: node.x[1]):
        super().__init__(iterable=iterable, key=key)

    def __str__(self):
        return str([x.x for x in self])

    def head_y(self):
        """ Return the point q from the list, with the smallest q_y """
        return self[0]

    def head_x(self):
        """ Return the point q from the list, with the smallest q_x """
        return self[-1]

    def next_y(self, s):
        """ Return the point q from the list, with the smallest q_y > s_y, for a given point s
        from the list """
        return self[self.index(s) + 1]

    def next_x(self, s):
        """ Return the point q from the list, with the smallest q_x > s_x, for a given point s
        from the list """
        return self[self.index(s) - 1]

    def outer_delimiter_y(self, p):
        """ Return the point q from the list, with the smallest q_y > p_y, such that q_x < p_x """
        i = self.bisect_left(p)
        while i < len(self) and self[i].x[0] >= p.x[0]:
            i += 1
        return self[i]

    def outer_delimiter_x(self, p):
        """ Return the point q from the list, with the smallest q_x > p_x, such that q_y < p_y """
        i = self.bisect_left(p) - 1
        while i > 0 and self[i].x[1] >= p.x[1]:
            i -= 1
        return self[i]

    def remove_dominated_y(self, p, s):
        """ For s = outer_delimiter_x(p), remove all points q, such that p* <= q* from the list,
        and return them sorted by ascending order of q_y """
        e = self.next_y(s)
        points_to_remove = []
        while p.x[0] <= e.x[0]:
            points_to_remove.append(e)
            e = self.next_y(e)

        for q in points_to_remove:
            self.remove(q)

        return points_to_remove

    def remove_dominated_x(self, p, s):
        """ For s = outer_delimiter_y(p), remove all points q, such that p* <= q* from the list,
        and return them sorted by ascending order of q_x """
        e = self.next_x(s)
        points_to_remove = []
        while p.x[1] <= e.x[1]:
            points_to_remove.append(e)
            e = self.next_x(e)

        for q in points_to_remove:
            self.remove(q)

        return points_to_remove

    def add_y(self, p, s):
        """ Insert point p into the list, if s_y < p_y < next_y(s)_y or p_y < head_y_y """
        if len(self) == 0:
            self.add(p)
        elif s.x[1] < p.x[1] < self.next_y(s).x[1]:
            self.add(p)
        elif p.x[1] < self.head_y().x[1] and s is None:
            self.add(p)

    def add_x(self, p, s):
        """ Insert point p into the list, if s_x < p_x < next_x(s)_x or p_x < head_x_x """
        if len(self) == 0:
            self.add(p)
        elif s.x[0] < p.x[0] < self.next_x(s).x[0]:
            self.add(p)
        elif p.x[0] < self.head_x().x[0] and s is None:
            self.add(p)


def my_lexsort(keys):
    """ Sort an array of keys in lexicographic order and return the indices.
    Equivalent to np.lexsort """
    idk_key_tuple = list(enumerate([list(x)[::-1] for x in zip(*keys)]))
    idk_key_tuple.sort(key=lambda x: x[1])
    return [x[0] for x in idk_key_tuple]
