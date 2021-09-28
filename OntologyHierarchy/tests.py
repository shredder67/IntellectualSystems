import unittest
from hierarchy import Hierarchy, AtrType

class TestAttrubuteAdding(unittest.TestCase):
    def setUp(self) -> None:
        self.hierarchy = Hierarchy()
        self.hierarchy.add_class("base")
        self.hierarchy.add_class("cl1", "base")
        self.hierarchy.add_class("cl2", "base")

    def test_add_num_single_atr(self):
        cl1 = self.hierarchy.root_class.subclasses[0]
        cl1.add_atr("num_sing", "NUM_SINGLE")
        self.assertIn("num_sing", cl1.attributes)
        self.assertEqual(cl1.attributes["num_sing"], AtrType.NUM_SINGLE)

    def test_add_num_multiple_atr(self):
        cl1 = self.hierarchy.root_class.subclasses[0]
        cl1.add_atr("num_mult", "NUM_MULTIPLE")
        self.assertIn("num_mult", cl1.attributes)
        self.assertEqual(cl1.attributes["num_mult"], AtrType.NUM_MULTIPLE)
    
    def test_add_str_single_atr(self):
        cl1 = self.hierarchy.root_class.subclasses[0]
        cl1.add_atr("str_sing", "STR_SINGLE")
        self.assertIn("str_sing", cl1.attributes)
        self.assertEqual(cl1.attributes["str_sing"], AtrType.STR_SINGLE)

    def test_add_str_multiple_atr(self):
        cl1 = self.hierarchy.root_class.subclasses[0]
        cl1.add_atr("str_mult", "STR_MULTIPLE")
        self.assertIn("str_mult", cl1.attributes)
        self.assertEqual(cl1.attributes["str_mult"], AtrType.STR_MULTIPLE)

    def test_add_single_link_atr(self):
        cl1 = self.hierarchy.root_class.subclasses[0]
        cl1.add_atr("link_sing", "LINK_SINGLE")
        self.assertIn("link_sing", cl1.attributes)
        self.assertEqual(cl1.attributes["link_sing"], AtrType.LINK_SINGLE)

    def test_add_multiple_link_atr(self):
        cl1 = self.hierarchy.root_class.subclasses[0]
        cl1.add_atr("link_mult", "LINK_MULTIPLE")
        self.assertIn("link_mult", cl1.attributes)
        self.assertEqual(cl1.attributes["link_mult"], AtrType.LINK_MULTIPLE)

    def tearDown(self) -> None:
        print('\n\n{0}\n'.format(self.hierarchy.to_str()))


if __name__ == '__main__':
    unittest.main()
