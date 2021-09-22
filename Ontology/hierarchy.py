import json
from enum import Enum

class Link:
    def __init__(this, type, classes):
        this.type = type
        this.classes = classes

    def __str__(this):
        res = '['
        for cls in this.classes:
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


    def __init__(this, name = None):
        this.id = HClass.id + 1
        HClass.id += 1
        this.name = this.name + str(HClass.id) if name is None else name
        this.attributes = dict() # atr_name : atr_type pairs
        this.subclasses = []
        this.instances = []

    # Adds attribute to attributes list, which stores attribute name and type
    # ! Important note: Link type (any) stores additional list of classes, with use of cutom Link class
    def add_atr(this, hier, name, str_type, *args):
        type = AtrType[str_type]

        if type is None:
            raise ValueError("Wrong attribute type!")

        if type == AtrType.LINK_SINGLE or type == AtrType.LINK_MULTIPLE:
            # Search for all classes in hierarchy
            links = [hier.find_class(cls_name) for cls_name in args]
            if None in links:
                raise ValueError("Class was not found in hierarchy!")
            this.attributes[name] = Link(type, links)
        else:
            this.attributes[name] = type


    def create_instance(this, values):
        inst = dict()
        i = 0
        for atr_name in this.attributes:
            # ? Type check implementation
            if(this.attributes[atr_name] == AtrType.STR_SINGLE):
                inst[atr_name] = float(values[i])
            if(this.attributes[atr_name] == AtrType.STR_MULTIPLE):
                inst[atr_name] = map(float, values[i].split(';'))
            if(this.attributes[atr_name] == AtrType.NUM_SINGLE):
                inst[atr_name] = values[i]
            if(this.attributes[atr_name] == AtrType.NUM_MULTIPLE):
                inst[atr_name] = map(str.strip, values[i].split(';'))
            if(this.attributes[atr_name] == AtrType.LINK_SINGLE):
                pass
            if(this.attributes[atr_name] == AtrType.LINK_MULTIPLE):
                pass
            inst[atr_name] = values[i]
            i += 1
        this.instances.append(inst)


    def __del__(this):
        if this.subclasses:
            for sub in this.subclasses:
                del sub



# Instance caches whole hierarchy, reads, saves and represents as string
class Hierarchy:
    name = "Hierarchy"
    root_class = None

    def __init__(this, name = None):
        this.name = this.name if name is None else name


    def find_class(this, class_name):
        if not this.root_class:
            return None
        # Breadth first search
        queue = []
        visited = {}
        queue.append(this.root_class)
        visited[this.root_class.name] = True
        while(len(queue) != 0):
            v = queue.pop()
            if(v.name == class_name):
                return v
            for sub in v.subclasses:
                if sub.name not in visited.keys():
                    queue.append(sub)
                    visited[sub] = True
        
        return None


    def add_class(this, class_name, class_parent = None):
        if this.root_class is None:
            this.root_class = HClass(class_name)
        elif class_parent is not None:
            parent_class = this.find_class(class_parent)
            if(parent_class):
                parent_class.subclasses.append(HClass(class_name))


    def _scan_hierarchy(this, cur, shift):
        sub = ''
        line = shift*'--' + cur.name

        if(cur.attributes):
            line += '('
            for k in cur.attributes.keys():
                line += k + ', '
            line = line[:-2] + ')'
        
        if(cur.subclasses):
            sub += line + '\n'
            for subcls in cur.subclasses:
                sub += this._scan_hierarchy(subcls, shift + 1)
        else:
            sub += line + '\n'
        return sub


    def _scan_hierarchy_with_instances(this, cur, shift):
        sub = ''
        line = shift*'--' + cur.name

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
                sub += this._scan_hierarchy(subcls, shift + 1)
        else:
            sub += line + '\n'
        return sub


    def to_str(this, with_instances = False):
        if with_instances:
            return this._scan_hierarchy_with_instances(this.root_class, 0)[:-1]
        else:
            return this._scan_hierarchy(this.root_class, 0)[:-1]


    def parse_from_json(this, filename):
        try:
            with open(filename, "r") as data:
                parsed_json = json.load(data)
                this.name = parsed_json["HierarchyName"]
                hierData = parsed_json["Structure"]

                for classdata in hierData:
                    cl = HClass(classdata["Name"])

                    # parse attributes
                    for name, batch in classdata["Attributes"].items():
                        args = list(batch.values()) # type or type and some additional values
                        cl.add_atr(this, name, args[0], args[1:-1])

                    # add into hierarchy
                    if this.root_class == None and classdata["Parent"] == None:
                        this.root_class = cl
                    else:
                        parent = this.find_class(classdata["Parent"])
                        if parent == None:
                            del this.root_class
                            raise ValueError(cl.name + " has no parent in hierarchy!")
                        
                        parent.subclasses.append(cl)
                
                return "Parsed hierarchy!"
        except ValueError as err:
            del this.root_class # clean tree before exiting
            return str(err.args[0])


    def __del__(this):
        del this.root_class

          



