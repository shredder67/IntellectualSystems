import json
from enum import Enum

class Link:
    def __init__(this, keys):
        this.keys = keys.copy()
        this.values = []


class AtrType(Enum):
    STR_SINGLE = 0
    STR_MULTIPLE = 1
    NUM_SINGLE = 2
    NUM_MULTIPLE = 3
    LINK = 4


# Instances hold default properties (id and name) and custom, that are added on the fly
class HClass:
    id = 0


    def __init__(this, name = None):
        this.id = HClass.id + 1
        HClass.id += 1
        this.name = this.name + str(HClass.id) if name is None else name
        this.subclasses = [] # instances created with attributes
        this.attributes = dict() # atr_name : atr_type pairs
        this.instances = []


    def _add_num_atr(this, name, cardinality):
        if name in this.attributes.keys():
            return
        if(cardinality == 'single'):
            this.attributes[name] = AtrType.NUM_SINGLE
        elif(cardinality == 'multiple'):
            this.attributes[name] = AtrType.NUM_MULTIPLE
    

    def _add_str_atr(this, name, cardinality):
        if name in this.attributes.keys():
            return
        if(cardinality == 'single'):
            this.attributes[name] = AtrType.STR_SINGLE
        elif(cardinality == 'multiple'):
            this.attributes[name] = AtrType.STR_MULTIPLE


    def _add_link_atr(this, name, classes):
        if name in this.attributes.keys():
            return
        this.attributes[name] = AtrType.LINK

    def add_atr(this, name, type, *args):
        if type == 'String':
            this._add_str_atr(name, *args)
        elif type == 'Num':
            this._add_num_atr(name, *args)
        elif type == 'Link':
            this._add_link_atr(name, *args)
        else:
            raise ValueError


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
                inst[atr_name] = map(strip, values[i].split(';'))
            if(this.attributes[atr_name] == AtrType.LINK):
                inst[atr_name] = 
            inst[atr_name] = values[i]
            i += 1
        this.instances.append(inst)


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

        if(cur.attributes):
            line += '('
            for k in cur.attributes.keys():
                line += k + ', '
            line = line[:-2] + ')'
        
        if(cur.instances):
            line += ':'
            for inst in cur.instances:
                line += '\n' + shift * '  ' + '['
                for atr_name in inst:
                    line += k + ', '
            line = line[:-2] + ']'
        
        if(cur.subclasses):
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


    # ? should class factory method, consturcting Hierarchy object based of reading file
    # File structure should be following:
    # {
    #     "Base":
    #     {
    #         "name": "SomeName",
    #         {
    #             "Subclasses" : {
    #                 ... (ever instanciable subclass should have "Attributes" field)
    #             }
    #         }
    #     }
    # }

    def _generate_hierarchy(this, cur):
        for sub in cur["Subclasses"]:
            scls = HClass(sub)
            if "Attribues" in sub:
                for atr in sub["Attributes"]:
                    if atr["type"] == 

    def parse_from_json(this, filename):
        with open(filename, "r") as data:
            hierData = json.load(data)
            root_name = hierData["Base"]["Name"]
            root = HClass(root_name)
            print(root)
            print(hierData)
            cur = root
            root.subclasses = _generate_hierarchy(cur)


