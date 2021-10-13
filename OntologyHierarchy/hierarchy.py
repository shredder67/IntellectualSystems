import json
from enum import Enum

# TODO: move __str__ logic from scan_hierarchy to class instances
# TODO: move comparison logic of Link to type definition and link it to ValueHolder comparison
# TODO: move message routing to separate Log object (and add coloring to messages)
# TODO: beautify command information
# TODO: make a damn report

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
    BASE = -1
    STR_SINGLE = 0
    STR_MULTIPLE = 1
    NUM_SINGLE = 2
    NUM_MULTIPLE = 3
    LINK_SINGLE = 4
    LINK_MULTIPLE = 5


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


class StringAttribute(Attribute):
    def __init__(self, name, atr_type):
        if atr_type == AtrType.STR_SINGLE or atr_type == AtrType.STR_MULTIPLE:
            super().__init__(name, atr_type)
        else:
            raise ValueError


class LinkAttribute(Attribute):
    def __init__(self, name, atr_type):
        if atr_type == AtrType.LINK_SINGLE or atr_type == AtrType.LINK_MULTIPLE:
            super().__init__(name, atr_type)
        else:
            raise ValueError


class AttributeFactory:
    @staticmethod
    def create_attribute(atr_name, atr_type):
        if atr_type == AtrType.NUM_SINGLE or atr_type == AtrType.NUM_MULTIPLE:
            return NumericAttribute(atr_name, atr_type)
        if atr_type == AtrType.STR_SINGLE or atr_type == AtrType.STR_MULTIPLE:
            return StringAttribute(atr_name, atr_type)
        if atr_type == AtrType.LINK_SINGLE or atr_type == AtrType.LINK_MULTIPLE:
            return LinkAttribute(atr_name, atr_type)


# Base Value Holder (used in instances)
class ValueHolder:
    def __init__(self, name, atr_type):
        self.name = name
        self.atr_type = atr_type

    def add_value(self, value):
        pass


class NumericValueHolder(ValueHolder):
    def __init__(self, name, atr_type, value):
        super().__init__(name, atr_type)
        self.add_value(value)

    def add_value(self, value):
        self.value = int(value)

    def __cmp__(self, other):
        if not isinstance(other, NumericValueHolder) and self.name != other.name:
            return NotImplemented

        if self.atr_type == AtrType.NUM_SINGLE:
            return
        else:
            pass


class StringValueHolder(ValueHolder):
    def __init__(self, name, atr_type, value):
        super().__init__(name, atr_type)
        self.add_value(value)

    def add_value(self, value):
        self.value = value

    def __cmp__(self, other):
        if not isinstance(other, StringValueHolder) and self.name != other.name:
            return NotImplemented

        if self.atr_type == AtrType.STR_SINGLE:
            pass
        else:
            pass


class LinkValueHolder(ValueHolder):
    def __init__(self, name, atr_type, value):
        super().__init__(name, atr_type)
        self.add_value(value)

    def add_value(self, value):
        self.value = Link(value)

    def __cmp__(self, other):
        if not isinstance(other, LinkValueHolder) and self.name != other.name:
            return NotImplemented

        if self.atr_type == AtrType.LINK_SINGLE:
            pass
        else:
            pass


class ValueHolderFactory:
    @staticmethod
    def create_value_holder(attribute, value):
        atr_type = attribute.atr_type
        if atr_type == AtrType.NUM_SINGLE or atr_type == AtrType.NUM_MULTIPLE:
            return NumericValueHolder(attribute.name, attribute.atr_type, value)
        if atr_type == AtrType.STR_SINGLE or atr_type == AtrType.STR_MULTIPLE:
            return StringValueHolder(attribute.name, attribute.atr_type, value)
        if atr_type == AtrType.LINK_SINGLE or atr_type == AtrType.LINK_MULTIPLE:
            return LinkValueHolder(attribute.name, attribute.atr_type, value)


# Instances hold default properties (id and name) and custom, that are added on the fly
class HClass:
    id = 0

    def __init__(self, name=None):
        self.id = HClass.id + 1
        HClass.id += 1
        self.name = "DefaultClassName" + str(HClass.id) if name is None else name
        self.attributes: list = []
        self.subclasses: list = []
        self.instances: dict = {}

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

    def has_atr(self, name):
        for atr in self.attributes:
            if atr.name == name:
                return True
        return False

    def create_instance(self, instance_name, atr_values):
        inst_values = {}
        for atr_name, value in atr_values.items():
            atr = self.get_atr_by_name(atr_name)
            if atr is None:
                raise ValueError
            value_holder = ValueHolderFactory.create_value_holder(atr, value)
            inst_values[value_holder.name] = value_holder # pair of type and value

        self.instances[instance_name] = inst_values


class LogicOperation:
    @staticmethod
    def _is_more(v1, v2):
        return v1 > v2
    
    @staticmethod
    def _is_more_or_equal(v1, v2):
        return v1 >= v2
    
    @staticmethod
    def _is_equal(v1, v2):
        return v1 == v2

    @staticmethod
    def _is_less_or_equal(v1, v2):
        return v1 <= v2

    @staticmethod
    def _is_less(v1, v2):
        return v1 < v2

    @classmethod
    def exec_operation(cls, v1, operation, v2) -> bool:
        return cls._exec_operation[operation](v1, v2)


LogicOperation._exec_operation = {
        '>':    LogicOperation._is_more,
        '>=':   LogicOperation._is_more_or_equal,
        '=':    LogicOperation._is_equal,
        '<=':   LogicOperation._is_less_or_equal,
        '<':    LogicOperation._is_less
}


class HierarchyQuery:

    def __init__(self, hierarchy):
        self.hierarchy = hierarchy

    def find_class(self, class_name):
        hier = self.hierarchy
        if not hier.root_class:
            return None
        # Breadth first search
        queue = []
        visited = {}
        queue.append(hier.root_class)
        visited[hier.root_class.name] = True
        while len(queue) != 0:
            v = queue.pop()
            if v.name == class_name:
                return v
            for sub in v.subclasses:
                if sub.name not in visited.keys():
                    queue.append(sub)
                    visited[sub] = True
    
    def filter_classes(self, root_class_name, filter):
        
        hier = self.hierarchy
        root = self.find_class(root_class_name)

        if root is None: return None

        # Breadth first search
        queue = []
        visited = {}
        filtered = []
        queue.append(root)
        visited[root.name] = True
        while len(queue) != 0:
            v = queue.pop()
            if filter(v):
                filtered.append(v)
            for sub in v.subclasses:
                if sub.name not in visited.keys():
                    queue.append(sub)
                    visited[sub] = True

        return filtered

    def filter_instances(self, classes, atr_filter, res):
        for cls in classes:
            for inst_name, attributes in cls.instances.items():
                if atr_filter(attributes):
                    res.append((inst_name, attributes))


# Instance caches whole hierarchy, reads, saves and represents as string
class Hierarchy:
    name = "Hierarchy"
    root_class = None

    def __init__(self, name=None):
        self._name = self.name if name is None else name
        self._query = HierarchyQuery(self)

    def find_class(self, class_name) -> HClass:
        return self._query.find_class(class_name)

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
            for atr in cur.attributes:
                line += atr.name + ', '
            line = line[:-2] + ')'

        if cur.instances:
            line += ':'
            line += '\n' + shift * '  ' + '['
            for inst_name in cur.instances:
                line += inst_name + ', '
            line = line[:-2] + ']'

        if cur.subclasses:
            sub += line + '\n'
            for subcls in cur.subclasses:
                sub += self._scan_hierarchy_with_instances(subcls, shift + 1)
        else:
            sub += line + '\n'
        return sub

    def to_str(self, with_instances=False) -> str:
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
                instances_data = parsed_json["Instances"]

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

                for instance in instances_data:
                    cl = self.find_class(instance["ClassName"])
                    if cl is None:
                        raise ValueError
                    inst_values = instance["Values"]
                    inst_name = inst_values["InstanceName"]
                    del inst_values["InstanceName"]
                    cl.create_instance(inst_name, inst_values)

        except ValueError as err:
            if self.root_class:
                del self.root_class  # clean tree before exiting
            raise err
    
    def query_to_str(self, query_result):
        res = 'Query result:\n'
        for inst in query_result:
            values = list(map(lambda holder : holder.value, inst[1].values()))
            res += '{}: {}\n'.format(inst[0], values)
        return res

    def query(self, cls_name, atr_name, relation, atr_reference) -> str:

        try:
            val = int(atr_reference)
        except(ValueError):
            val = atr_reference

        # Search for all classes with atr_name from query_root
        filtered_classes = self._query.filter_classes(cls_name, lambda cls : cls.has_atr(atr_name))
        # Filter instances of classes with predicate
        filtered_instances = []
        self._query.filter_instances(
            filtered_classes,
            lambda attributes: LogicOperation.exec_operation(attributes[atr_name].value, relation, val),
            filtered_instances
        )
        # Form a string from all instances and return
        str_res = self.query_to_str(filtered_instances)
        return str_res