import json
from enum import Enum
from sys import addaudithook

# TODO: Сделать множественное наследование класса (Parent -> Parents), для каждого родителя продублировать класс

# Value holder for link attributes
class Link:
    def __init__(self, inst_names):
        self.inst_names = set(inst_names)

    def __eq__(self, other):
        if isinstance(other, str):
            return other in self.inst_names

        if isinstance(other, list):
            return set(other) == self.inst_names

        if len(self.inst_names) != len(other.inst_names):
            return False

        return self.inst_names == other.inst_names

    def __str__(self):
        return str(self.inst_names)

    def __repr__(self):
        return str(self)


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
        self.additional_parents = None

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
        if atr_values:
            for atr_name, value in atr_values.items():
                atr = self.get_atr_by_name(atr_name)
                if atr is None:
                    raise ValueError
                value_holder = ValueHolderFactory.create_value_holder(atr, value)
                inst_values[value_holder.name] = value_holder  # pair of type and value

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
    hierarchy = None

    @classmethod
    def find_class(cls, class_name):
        if not cls.hierarchy.root_class:
            return None
        # Breadth first search
        queue = []
        visited = {}
        queue.append(cls.hierarchy.root_class)
        visited[cls.hierarchy.root_class.name] = True
        while len(queue) != 0:
            v = queue.pop()
            if v.name == class_name:
                return v
            for sub in v.subclasses:
                if sub.name not in visited.keys():
                    queue.append(sub)
                    visited[sub] = True

    @classmethod
    def filter_classes(cls, lambda_filter, root_class_name=None):
        if root_class_name:
            root = cls.find_class(root_class_name)
        else:
            root = cls.hierarchy.root_class

        # Breadth first search
        queue = []
        visited = {}
        filtered = []
        queue.append(root)
        visited[root.name] = True
        while len(queue) != 0:
            v = queue.pop()
            if lambda_filter(v):
                filtered.append(v)
            for sub in v.subclasses:
                if sub.name not in visited.keys():
                    queue.append(sub)
                    visited[sub] = True

        return filtered

    @classmethod
    def filter_and_apply(cls, lambda_filter, lambda_action, root_class_name=None):
        if root_class_name:
            root = cls.find_class(root_class_name)
        else:
            root = cls.hierarchy.root_class

        # Breadth first search
        queue = []
        visited = {}
        queue.append(root)
        visited[root.name] = True
        while len(queue) != 0:
            v = queue.pop()
            if lambda_filter(v):
                lambda_action(v)
            for sub in v.subclasses:
                if sub.name not in visited.keys():
                    queue.append(sub)
                    visited[sub] = True

    @staticmethod
    def filter_instances(classes, atr_filter, res):
        for cls in classes:
            for inst_name, attributes in cls.instances.items():
                if atr_filter(attributes):
                    res.append((inst_name, cls.name, attributes))

    @staticmethod
    def query_to_str(query_result):
        res = 'Query result:\n'
        for inst in query_result:
            values = list(map(lambda holder: holder.value, inst[2].values()))
            res += '{} : {}\n{}\n'.format(inst[0], inst[1], values)
        return res


# Instance caches whole hierarchy, reads, saves and represents as string
class Hierarchy:
    name = "Hierarchy"
    root_class = None

    def __init__(self, name=None):
        self._name = self.name if name is None else name
        self._queries = None
        HierarchyQuery.hierarchy = self

    def find_class(self, class_name) -> HClass:
        return HierarchyQuery.find_class(class_name)

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
                    if self.root_class is None and classdata["Parents"] is None:
                        self.root_class = cl
                    else:
                        # inject as subclass for [0] parent
                        parent = self.find_class(classdata["Parents"][0])
                        if parent is None:
                            del self.root_class
                            raise ValueError(cl.name + " has no parent in hierarchy!")

                        cl.additional_parents = classdata["Parents"][1:]
                        parent.subclasses.append(cl)

                # secondary subclasses injection
                def add_to_parents(sub):
                    for new_parent in sub.additional_parents:
                        p = HierarchyQuery.find_class(new_parent)
                        p.subclasses.append(sub)
                    sub.additional_parents = None

                HierarchyQuery.filter_and_apply(
                    lambda some_class: some_class.additional_parents is not None,
                    lambda_action=add_to_parents
                )

                for instance in instances_data:
                    cl = self.find_class(instance["ClassName"])
                    if cl is None:
                        raise ValueError
                    inst_values = instance["Values"]
                    inst_name = inst_values["InstanceName"]
                    del inst_values["InstanceName"]
                    cl.create_instance(inst_name, inst_values)

                if "Queries" in parsed_json:
                    self._queries = parsed_json["Queries"]

        except ValueError as err:
            if self.root_class:
                del self.root_class  # clean tree before exiting
            raise err

    def query(self, cls_name, atr_name, relation, atr_reference) -> str:
        try:
            val = int(atr_reference)
        except ValueError:
            val = atr_reference

        # Search for all classes with atr_name from query_root
        filtered_classes = HierarchyQuery.filter_classes(root_class_name=cls_name,
                                                         lambda_filter=lambda cls: cls.has_atr(atr_name))
        # Filter instances of classes with predicate
        filtered_instances = []
        HierarchyQuery.filter_instances(
            filtered_classes,
            lambda attributes: LogicOperation.exec_operation(attributes[atr_name].value, relation, val),
            filtered_instances
        )
        # Form a string from all instances and return
        return HierarchyQuery.query_to_str(filtered_instances)

    def run_queries(self):
        res = ''
        if self._queries:
            for _query in self._queries:
                res += self.query(_query["In"], _query["Attribute"], _query["Relation"], _query["Value"]) + '\n\n'
        else:
            res = 'No queries stored!  '
        return res[:-2]

