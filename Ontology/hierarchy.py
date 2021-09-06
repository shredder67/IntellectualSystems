# Instances hold default properties (id and name) and custom, that are added on the fly
class HClass:
    id = -1
    name = "Class"
    parent = None
    subclasses = []


    def __init__(this, name = None):
        this.id = HClass.id + 1
        HClass.id += 1
        this.name = this.name + str(HClass.id) if name is None else name

# Instance caches whole hierarchy, reads, saves and represents as string
class Hierarchy:
    name = "Hierarchy"
    root_class = None

    def __init__(this, name = None):
        this.name = this.name if name is None else name


    def find_class(this, class_name):
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
            

    def save(filename, path):
        pass


    def load(path):
        pass


    def _scan_hierarchy(this, res, cur, shift):
        line = shift + cur.name
        if(len(cur.subclasses) != 0):
            line + ':'
            res += line + '\n'
            for sub in cur.subclasses:
                res += this._scan_hierarchy(this, sub, shift + '\t')
        else:
            res += line + '\n'
        return res


    def __str__(this):
        res = ''
        return this._scan_hierarchy(res, this.root_class, '')
