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


# Instances hold default properties (id and name) and custom, that are added on the fly
class HClass:
    id = 0

    def __init__(self, name=None):
        self.id = HClass.id + 1
        HClass.id += 1
        self.name = "DefaultClassName" + str(HClass.id) if name is None else name
        self.attributes = dict()  # atr_name : atr_type pairs
        self.subclasses = []
        self.instances = []

    # Adds attribute to attributes list, which stores attribute name and type
    def add_atr(self, name, str_type):

        if str_type not in AtrType.__dict__.keys():
            raise ValueError("Wrong attribute type!")

        atr_type = AtrType[str_type]
        self.attributes[name] = atr_type

    # TODO: Fix this method and abstract it from input format
    def create_instance(self, values):
        inst = dict()
        i = 0
        atr_names = self.attributes.keys()
        for value in values:
            # ? Type check implementation
            # TODO: load values into memory
            i += 1
        self.instances.append(inst)

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
            for k in cur.attributes.keys():
                line += k + ', '
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
