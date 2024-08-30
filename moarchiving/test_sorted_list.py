import unittest
from moarchiving_utils import MySortedList, DLNode


class MyTestCase(unittest.TestCase):
    def test_init(self):
        sl = MySortedList()
        self.assertEqual(str(sl), "[]")

        sl = MySortedList([DLNode([3, 0]), DLNode([1, 2]), DLNode([0, 3]), DLNode([2, 1])])
        self.assertEqual(str(sl), "[[3, 0], [2, 1], [1, 2], [0, 3]]")

    def test_add(self):
        sl = MySortedList()
        self.assertEqual(str(sl), "[]")
        sl.add(DLNode([3, 0]))
        self.assertEqual(str(sl), "[[3, 0]]")
        sl.add(DLNode([1, 2]))
        self.assertEqual(str(sl), "[[3, 0], [1, 2]]")
        sl.add(DLNode([0, 3]))
        self.assertEqual(str(sl), "[[3, 0], [1, 2], [0, 3]]")
        sl.add(DLNode([2, 1]))
        self.assertEqual(str(sl), "[[3, 0], [2, 1], [1, 2], [0, 3]]")

    def test_remove(self):
        n1 = DLNode([3, 0])
        n2 = DLNode([1, 2])
        n3 = DLNode([0, 3])
        n4 = DLNode([2, 1])
        sl = MySortedList([n1, n2, n3, n4])
        self.assertEqual(str(sl), "[[3, 0], [2, 1], [1, 2], [0, 3]]")
        sl.remove(n1)
        self.assertEqual(str(sl), "[[2, 1], [1, 2], [0, 3]]")
        sl.remove(n2)
        self.assertEqual(str(sl), "[[2, 1], [0, 3]]")
        sl.remove(n3)
        self.assertEqual(str(sl), "[[2, 1]]")
        sl.remove(n4)
        self.assertEqual(str(sl), "[]")

    def test_head(self):
        sl = MySortedList([DLNode([3, 0]), DLNode([1, 2]), DLNode([0, 3]), DLNode([2, 1])])
        self.assertEqual(sl.head_y().x, [3, 0])
        self.assertEqual(sl.head_x().x, [0, 3])

    def test_next(self):
        n1 = DLNode([3, 0])
        n2 = DLNode([1, 2])
        n3 = DLNode([0, 3])
        n4 = DLNode([2, 1])
        sl = MySortedList([n1, n2, n3, n4])

        self.assertEqual(sl.next_y(n1), n4)
        self.assertEqual(sl.next_y(n4), n2)
        self.assertEqual(sl.next_y(n2), n3)

        self.assertEqual(sl.next_x(n3), n2)
        self.assertEqual(sl.next_x(n2), n4)
        self.assertEqual(sl.next_x(n4), n1)

    def test_outer_delimiter(self):
        n1 = DLNode([3, 0])
        n2 = DLNode([1, 2])
        n3 = DLNode([0, 3])
        n4 = DLNode([2, 1])
        sl = MySortedList([n1, n2, n3, n4])

        self.assertEqual(sl.outer_delimiter_y(DLNode([1.5, 1.5])), n2)
        self.assertEqual(sl.outer_delimiter_y(DLNode([0.5, 1.5])), n3)
        self.assertEqual(sl.outer_delimiter_y(DLNode([1.5, 0.5])), n2)

        self.assertEqual(sl.outer_delimiter_x(DLNode([1.5, 1.5])), n4)
        self.assertEqual(sl.outer_delimiter_x(DLNode([0.5, 1.5])), n4)
        self.assertEqual(sl.outer_delimiter_x(DLNode([1.5, 0.5])), n1)
        self.assertEqual(sl.outer_delimiter_x(DLNode([-1, 4])), n3)

    def test_remove_dominated(self):
        n1 = DLNode([3, 0])
        n2 = DLNode([1, 2])
        n3 = DLNode([0, 3])
        n4 = DLNode([2, 1])

        sl = MySortedList([n1, n2, n3, n4])
        p = DLNode([1.5, 0.5])
        s = sl.outer_delimiter_x(p)
        points_to_remove = sl.remove_dominated_y(p, s)
        self.assertEqual(points_to_remove, [n4])
        self.assertEqual(str(sl), "[[3, 0], [1, 2], [0, 3]]")

        sl = MySortedList([n1, n2, n3, n4])
        p = DLNode([0.5, 0.5])
        s = sl.outer_delimiter_x(p)
        points_to_remove = sl.remove_dominated_y(p, s)
        self.assertEqual(points_to_remove, [n4, n2])
        self.assertEqual(str(sl), "[[3, 0], [0, 3]]")

        sl = MySortedList([n1, n2, n3, n4])
        p = DLNode([1.5, 0.5])
        s = sl.outer_delimiter_y(p)
        points_to_remove = sl.remove_dominated_x(p, s)
        self.assertEqual(points_to_remove, [n4])
        self.assertEqual(str(sl), "[[3, 0], [1, 2], [0, 3]]")

        sl = MySortedList([n1, n2, n3, n4])
        p = DLNode([0.5, 0.5])
        s = sl.outer_delimiter_y(p)
        points_to_remove = sl.remove_dominated_x(p, s)
        self.assertEqual(points_to_remove, [n2, n4])
        self.assertEqual(str(sl), "[[3, 0], [0, 3]]")

    def test_add_xy(self):
        # TODO: Implement this test
        pass


if __name__ == '__main__':
    unittest.main()
