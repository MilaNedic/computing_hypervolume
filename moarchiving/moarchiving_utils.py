
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


def my_lexsort(keys):
    """ Sort an array of keys in lexicographic order and return the indices.
    Equivalent to np.lexsort """
    idk_key_tuple = list(enumerate([list(x)[::-1] for x in zip(*keys)]))
    idk_key_tuple.sort(key=lambda x: x[1])
    return [x[0] for x in idk_key_tuple]
