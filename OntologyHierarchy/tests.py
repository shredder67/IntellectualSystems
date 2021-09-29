import unittest
from hierarchy import Hierarchy, AtrType


class TestAttrubuteAdding(unittest.TestCase):
    def setUp(self) -> None:
        self.hierarchy = Hierarchy()
        self.hierarchy.add_class("base")
        self.hierarchy.add_class("cl1", "base")
        self.hierarchy.add_class("cl2", "base")
        self.atr_name = "test"

    def test_add_num_single_atr(self):
        test_type = AtrType.NUM_SINGLE
        cl1 = self.hierarchy.root_class.subclasses[0]
        cl1.add_atr(self.atr_name, "NUM_SINGLE")
        self.assertEquals(self.atr_name, cl1.attributes[0].name)
        self.assertEqual(test_type, cl1.attributes[0].atr_type)

    def test_add_num_multiple_atr(self):
        test_type = AtrType.NUM_MULTIPLE
        cl1 = self.hierarchy.root_class.subclasses[0]
        cl1.add_atr(self.atr_name, "NUM_MULTIPLE")
        self.assertEquals(self.atr_name, cl1.attributes[0].name)
        self.assertEqual(test_type, cl1.attributes[0].atr_type)

    def test_add_str_single_atr(self):
        test_type = AtrType.STR_SINGLE
        cl1 = self.hierarchy.root_class.subclasses[0]
        cl1.add_atr(self.atr_name, "STR_SINGLE")
        self.assertEquals(self.atr_name, cl1.attributes[0].name)
        self.assertEqual(test_type, cl1.attributes[0].atr_type)

    def test_add_str_multiple_atr(self):
        test_type = AtrType.STR_MULTIPLE
        cl1 = self.hierarchy.root_class.subclasses[0]
        cl1.add_atr(self.atr_name, "STR_MULTIPLE")
        self.assertEquals(self.atr_name, cl1.attributes[0].name)
        self.assertEqual(test_type, cl1.attributes[0].atr_type)

    def test_add_single_link_atr(self):
        test_type = AtrType.LINK_SINGLE
        cl1 = self.hierarchy.root_class.subclasses[0]
        cl1.add_atr(self.atr_name, "LINK_SINGLE")
        self.assertEquals(self.atr_name, cl1.attributes[0].name)
        self.assertEqual(test_type, cl1.attributes[0].atr_type)

    def test_add_multiple_link_atr(self):
        test_type = AtrType.LINK_MULTIPLE
        cl1 = self.hierarchy.root_class.subclasses[0]
        cl1.add_atr(self.atr_name, "LINK_MULTIPLE")
        self.assertEquals(self.atr_name, cl1.attributes[0].name)
        self.assertEqual(test_type, cl1.attributes[0].atr_type)


if __name__ == '__main__':
    unittest.main()
