import json

class Link:

    def __init__(this, keys):
        this.keys = keys.copy()
        this.values = []

# Instances hold default properties (id and name) and custom, that are added on the fly
class HClass:
    id = 0
    
    def __init__(this, name = None):
        this.id = HClass.id + 1
        HClass.id += 1
        this.name = this.name + str(HClass.id) if name is None else name
        this.subclasses = []
        this.attributes = dict()
        this.instances = []


    def add_num_atr(this, name, cardinality):
        if name in this.attributes.keys():
            return
        if(cardinality == 'single'):
            this.attributes[name] = ''
        elif(cardinality == 'multiple'):
            this.attributes[name] = []
    

    def add_str_atr(this, name, cardinality):
        if name in this.attributes.keys():
            return
        if(cardinality == 'single'):
            this.attributes[name] = -1
        elif(cardinality == 'multiple'):
            this.attributes[name] = []


    def add_link_atr(this, name, classes):
        if name in this.attributes.keys():
            return
        this.attributes[name] = Link(classes)


    def get_atr_val(this, name):
        if name not in this.attributes.keys():
            return None
        atr = this.attributes[name]
        if(isinstance(atr, (int, float))):
            pass
        elif(isinstance(atr, str)):
            pass
        else:
            pass

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
            

    def save(this, filename, path):
        pass


    def load(this, path):
        pass


    def _scan_hierarchy(this, cur, shift):
        sub = ''
        line = shift*'--' + ' ' + cur.name
        if(cur.attributes):
            line += '('
            for k in cur.attributes.keys():
                line += k + ' '
            line[-1] = ')'
        if(cur.subclasses):
            line + ':'
            sub += line + '\n'
            for subcls in cur.subclasses:
                sub += this._scan_hierarchy(subcls, shift + 1)
        else:
            sub += line + '\n'
        return sub


    def __str__(this):
        return this._scan_hierarchy(this.root_class, 0)
