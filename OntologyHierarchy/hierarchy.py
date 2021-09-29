import json
from enum import Enum


# Value holder for link attributes
class Link:
    def __init__(self, classes):
        self.classes = classes

    def __eq__(self, other):
        if not isinstance(other, Link):
            return NotImplemented

        if len(other.classes) != len(self.classes):
            return False

        i = 0
        while i < len(self.classes):
            if self.classes[i] != other.classes[i]:
                return False
        return True

    def __str__(self):
        res = '['
        for cls in self.classes:
            res += ' ' + cls.name + ','
        return res[:-1]


class AtrType(Enum):
    STR_SINGLE = 0
    STR_MULTIPLE = 1
    NUM_SINGLE = 2
    NUM_MULTIPLE = 3
    LINK_SINGLE = 4
    LINK_MULTIPLE = 5

# TODO Rework ValueHolder dependency so I can use polymorph methods for data comparison
# Base Attribute class
class Attribute:
    def __init__(self, name, atr_type):
        self.name = name
        self.atr_type = atr_type


class NumericAttribute(Attribute):
    def __init__(self, name, atr_type):
        if atr_type == AtrType.NUM_SINGLE or atr_type == AtrType.NUM_MULTIPLE:
            super().__init__(name, atr_type)
        else:
            raise ValueError


class NumericValueHolder(NumericAttribute):
    def __init__(self, name, atr_type, value):
        super().__init__(name, atr_type)
        self.value = value

    def __cmp__(self, other):
        if not isinstance(other, NumericValueHolder) and self.name != other.name:
            return NotImplemented

        if self.atr_type == AtrType.NUM_SINGLE:
            pass
        else:
            pass


class StringAttribute(Attribute):
    def __init__(self, name, atr_type):
        if atr_type == AtrType.STR_SINGLE or atr_type == AtrType.STR_MULTIPLE:
            super().__init__(name, atr_type)
        else:
            raise ValueError


class StringValueHolder(StringAttribute):
    def __init__(self, name, atr_type, value):
        super().__init__(name, atr_type)
        self.value = value

    def __cmp__(self, other):
        if not isinstance(other, StringValueHolder) and self.name != other.name:
            return NotImplemented

        if self.atr_type == AtrType.STR_SINGLE:
            pass
        else:
            pass


class LinkAttribute(Attribute):
    def __init__(self, name, atr_type):
        if atr_type == AtrType.LINK_SINGLE or atr_type == AtrType.LINK_MULTIPLE:
            super().__init__(name, atr_type)
        else:
            raise ValueError


class LinkValueHolder(Attribute):
    def __init__(self, name, atr_type, value):
        super().__init__(name, atr_type)
        self.value = Link(value)

    def __cmp__(self, other):
        if not isinstance(other, LinkValueHolder) and self.name != other.name:
            return NotImplemented

        if self.atr_type == AtrType.LINK_SINGLE:
            pass
        else:
            pass


class AttributeFactory:
    @staticmethod
    def create_attribute(atr_name, atr_type):
        if atr_type == AtrType.NUM_SINGLE or atr_type == AtrType.NUM_MULTIPLE:
            return NumericAttribute(atr_name, atr_type)
        if atr_type == AtrType.STR_SINGLE or atr_type == AtrType.STR_MULTIPLE:
            return StringAttribute(atr_name, atr_type)
        if atr_type == AtrType.LINK_SINGLE or atr_type == AtrType.LINK_MULTIPLE:
            return LinkAttribute(atr_name, atr_type)


class ValueHolderFactory:
    @staticmethod
    def create_value_holder(attribute, value):
        if attribute(isinstance(attribute, NumericAttribute)):
            return NumericValueHolder(attribute.name, attribute.atr_type, value)
        if attribute(isinstance(attribute, StringAttribute)):
            return NumericValueHolder(attribute.name, attribute.atr_type, value)
        if attribute(isinstance(attribute, LinkAttribute)):
            return NumericValueHolder(attribute.name, attribute.atr_type, value)


# Instances hold default properties (id and name) and custom, that are added on the fly
class HClass:
    id = 0

    def __init__(self, name=None):
        self.id = HClass.id + 1
        HClass.id += 1
        self.name = "DefaultClassName" + str(HClass.id) if name is None else name
        self.attributes: list = []
        self.subclasses: list = []
        self.instances: list = []

    def add_atr(self, name, str_type):
        if str_type not in AtrType.__dict__.keys():
            raise ValueError("Wrong attribute type!")

        atr_type = AtrType[str_type]
        self.attributes.append(AttributeFactory.create_attribute(name, atr_type))

    def get_atr_by_name(self, name):
        for atr in self.attributes:
            if atr.name == name:
                return atr
        return None

    def create_instance(self, instance_name, atr_values):
        # values : {atr_name : value (single value or list)}
        # TODO add this data to file
        inst_attributes = []
        for atr_name, value in atr_values.items():
            atr = self.get_atr_by_name(atr_name)
            if atr is None:
                raise ValueError
            inst_attributes.append(ValueHolderFactory.create_value_holder(atr, value))

        self.instances[instance_name] = inst_attributes

    def __del__(self):
        if self.subclasses:
            for sub in self.subclasses:
                del sub


# Instance caches whole hierarchy, reads, saves and represents as string
class Hierarchy:
    name = "Hierarchy"
    root_class = None

    def __init__(self, name=None):
        self.name = self.name if name is None else name

    def find_class(self, class_name):
        if not self.root_class:
            return None
        # Breadth first search
        queue = []
        visited = {}
        queue.append(self.root_class)
        visited[self.root_class.name] = True
        while len(queue) != 0:
            v = queue.pop()
            if v.name == class_name:
                return v
            for sub in v.subclasses:
                if sub.name not in visited.keys():
                    queue.append(sub)
                    visited[sub] = True

        return None

    def add_class(self, class_name, class_parent=None):
        if self.root_class is None:
            self.root_class = HClass(class_name)
        elif class_parent is not None:
            parent_class = self.find_class(class_parent)
            if parent_class:
                parent_class.subclasses.append(HClass(class_name))

    def _scan_hierarchy(self, cur, shift):
        sub = ''
        line = shift * '--' + cur.name

        if cur.attributes:
            line += '('
            for atr in cur.attributes:
                line += atr.name + ', '
            line = line[:-2] + ')'

        if cur.subclasses:
            sub += line + '\n'
            for subcls in cur.subclasses:
                sub += self._scan_hierarchy(subcls, shift + 1)
        else:
            sub += line + '\n'
        return sub

    def _scan_hierarchy_with_instances(self, cur, shift):
        sub = ''
        line = shift * '--' + cur.name

        if cur.attributes:
            line += '('
            for k in cur.attributes.keys():
                line += k + ', '
            line = line[:-2] + ')'

        if cur.instances:
            line += ':'
            for inst in cur.instances:
                line += '\n' + shift * '  ' + '['
                for atr_name in inst:
                    line += k + ', '
            line = line[:-2] + ']'

        if cur.subclasses:
            sub += line + '\n'
            for subcls in cur.subclasses:
                sub += self._scan_hierarchy(subcls, shift + 1)
        else:
            sub += line + '\n'
        return sub

    def to_str(self, with_instances=False):
        if with_instances:
            return self._scan_hierarchy_with_instances(self.root_class, 0)[:-1]
        else:
            return self._scan_hierarchy(self.root_class, 0)[:-1]

    def parse_from_json(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as data:
                parsed_json = json.load(data)
                self.name = parsed_json["HierarchyName"]
                hier_data = parsed_json["Structure"]

                for classdata in hier_data:
                    cl = HClass(classdata["Name"])

                    # parse attributes
                    for name, batch in classdata["Attributes"].items():
                        cl.add_atr(name, batch["type"])

                    # add into hierarchy
                    if self.root_class is None and classdata["Parent"] is None:
                        self.root_class = cl
                    else:
                        parent = self.find_class(classdata["Parent"])
                        if parent is None:
                            del self.root_class
                            raise ValueError(cl.name + " has no parent in hierarchy!")

                        parent.subclasses.append(cl)

        except ValueError as err:
            if self.root_class:
                del self.root_class  # clean tree before exiting
            raise err

    def __del__(self):
        if self.root_class:
            del self.root_class
