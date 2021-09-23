import json
from enum import Enum


class Link:
    def __init__(self, classes):
        self.classes = classes

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
        self.name = "Class" + str(HClass.id) if name is None else name
        self.attributes = dict()  # atr_name : atr_type pairs
        self.subclasses = []
        self.instances = []

    # Adds attribute to attributes list, which stores attribute name and type
    # ! Important note: Link type (any) stores additional list of classes, with use of custom Link class
    def add_atr(self, hier_obj, name, str_type, *args):
        atr_type = AtrType[str_type]

        if atr_type is None:
            raise ValueError("Wrong attribute type!")

        if atr_type == AtrType.LINK_SINGLE or atr_type == AtrType.LINK_MULTIPLE:
            # Search for all classes in hierarchy
            # TODO : Fix search for objects down in the hierarchy
            # Possible solution: fill hierarchy with strings, then walk over all Links and replace them with
            # actual object references
            # Second possible solution: sprint through class names/subclasses, create hierarchy structure
            # then loop over all objects and fill the attributes (with correct Links)
            links = [hier_obj.find_class(cls_name) for cls_name in args]
            if None in links:
                raise ValueError("Class was not found in hierarchy!")
            self.attributes[name] = (atr_type, Link(links))
        else:
            self.attributes[name] = atr_type

    def create_instance(self, values):
        inst = dict()
        i = 0
        for atr_name in self.attributes:
            # ? Type check implementation
            if self.attributes[atr_name] == AtrType.STR_SINGLE:
                inst[atr_name] = float(values[i])
            if self.attributes[atr_name] == AtrType.STR_MULTIPLE:
                inst[atr_name] = map(float, values[i].split(';'))
            if self.attributes[atr_name] == AtrType.NUM_SINGLE:
                inst[atr_name] = values[i]
            if self.attributes[atr_name] == AtrType.NUM_MULTIPLE:
                inst[atr_name] = map(str.strip, values[i].split(';'))
            if self.attributes[atr_name] == AtrType.LINK_SINGLE:
                pass
            if self.attributes[atr_name] == AtrType.LINK_MULTIPLE:
                pass
            inst[atr_name] = values[i]
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
                        atr_type = batch["type"]
                        value = batch["value"] if "value" in batch else None
                        cl.add_atr(self, name, atr_type, value)

                    # add into hierarchy
                    if self.root_class is None and classdata["Parent"] is None:
                        self.root_class = cl
                    else:
                        parent = self.find_class(classdata["Parent"])
                        if parent is None:
                            del self.root_class
                            raise ValueError(cl.name + " has no parent in hierarchy!")

                        parent.subclasses.append(cl)

                return "Parsed hierarchy!"
        except ValueError as err:
            del self.root_class  # clean tree before exiting
            return str(err.args[0])

    def __del__(self):
        del self.root_class
