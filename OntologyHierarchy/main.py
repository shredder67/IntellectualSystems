# Program creates class hierarchy and instances, reads it from JSON file.
# Allows to perform query throw the "knowledge base" of instances
# Instances have attributes of string, numerical and instance types
# Type info() for command information

# TODO: Fix RUNTIME instance creation (currently wrong input format, need to parse into dict like {atr_name : value})

import signal
import sys
import re
from os import path, system as os_system, name as os_name
from hierarchy import Hierarchy


# Set up Ctrl-C handler for exiting program
def ctrl_c_handler(sig, frame):
    print('\nExiting...')
    sys.exit(0)


signal.signal(signal.SIGINT, ctrl_c_handler)


# Static class, stores all commands and handle functions
class CommandHandler:
    # Hierarchy object
    HierarchyObject = None

    commands_desc = dict({
        'info':         '() - prints all commands info',
        'create':       '(hierarchy_name) - creates a new hiearchy and loads it in memory',
        'print':        '() - prints the current hierarchy',
        'add_cls':      '(name, super_class = None) - creates new class * TODO for multiple',
        'add_atr':      '(name, type) - adds attribute to class\ntype list:\n\tNUM_SINGLE - single number\n\t'
                        'NUM_MULTIPLE - number array\n\tSTR_SINGLE - single string\n\tSTR_MULTIPLE - string array'
                        'LINK_SINGLE - single link to other class/classes\n\tLINK_MULTIPLE - multiple links to other'
                        'class/classes',
        'query':        '(root_class_name, atr_name, relation (one of >=, >, =, <, <=), value)',
        'run_q':        '() - runs queries read stored in hierarchy (read from json)',
        # 'inst':        '() - creates an instance of class with entered parameters'
        #                'NOTE: use like this: cls_name.inst(args)',
        'print_inst':   '() - prints all instances in hierarchy',
        #  'save':         '(path) - saves hierarchy as json file',
        'open':         '(path) - opens exiting hierarchy (from json) and instances',
        'cls':         '() - cleans the screen'
    })
    commands = commands_desc.keys()

    # Handles function calls
    def handle(self, command_name, arg):
        mes = None
        if command_name == 'info':
            self._info()
        elif command_name == 'create':
            self._create(arg)
        elif command_name == 'open':
            mes = self._open(arg)
        elif command_name == 'cls':
            self._cls()

        elif self.HierarchyObject is None:
            mes = "Hierarchy has not been created/opened yet!"

        elif command_name == 'add_cls':
            mes = self._add_class(arg)
        elif command_name == 'print':
            self._print()
        elif command_name == 'print_inst':
            self._print_inst()
        elif command_name == 'query':
            self._query(arg)
        elif command_name == 'run_q':
            self._run_queries()
        elif command_name == 'save':
            self._save(arg)
        return mes

    # Handles function calls related to classes in hierarchy in format cls_name.command(args)
    def handle_cls(self, cls_name, command_name, args):
        cls = self.HierarchyObject.find_class(cls_name)
        if not cls:
            mes = 'No such class in hierarchy!'
            return mes
        if command_name == 'add_atr':
            mes = self._add_atr(cls, args)
        elif command_name == 'inst':
            mes = self._inst(cls, args)
        mes = "Something went wrong..."
        return mes

    def _info(self):
        for key in self.commands_desc:
            print(key + self.commands_desc[key])

    def _create(self, arg):
        self.HierarchyObject = Hierarchy(arg)
        return 'Hierarchy created!'

    def _add_class(self, arg):
        args = arg.split(',')
        if (len(args) > 1):
            self.HierarchyObject.add_class(args[0].strip(), args[1].strip())
        else:
            self.HierarchyObject.add_class(args[0].strip())
        return 'Added class to hierarchy!'

    def _add_atr(self, cls, arg):
        args = list(map(str.strip, arg.split(',')))
        try:
            cls.add_atr(*args)
        except IndexError:
            return 'Wrong amount of arguments!'
        except ValueError as err:
            return str(err.args[0])
        return 'Attribute ' + args[0] + ' added to ' + cls.name

    def _inst(self, cls, arg):
        # arg is value, value, value in defined order
        values = list(map(str.strip, arg.split(',')))
        if len(values) == 1:
            values.append(None)
        cls.create_instance(values[0], values[1:])
        return 'Instance created!'

    def _print(self):
        print(self.HierarchyObject.to_str())

    def _print_inst(self):
        print(self.HierarchyObject.to_str(True))

    def _save(self, arg):
        pass

    def _query(self, arg):
        values = list(map(str.strip, arg.split(',')))
        res = self.HierarchyObject.query(*values)
        print(res)

    def _run_queries(self):
        res = self.HierarchyObject.run_queries()
        print(res)

    def _open(self, arg):
        if path.exists(arg):
            self.HierarchyObject = Hierarchy()
            self.HierarchyObject.parse_from_json(arg)
            return 'Hierarchy parsed!'
        else:
            return 'Wrong path!'

    def _cls(self):
        os_system('cls' if os_name == 'nt' else 'clear')


# command(args)
# args : arg1, arg2, ..., argn or {... key : val ...}
comHandler = CommandHandler()
command_pattern = re.compile('^([A-Za-z0-9А-Яа-я_]*)\(([^)]*)\)$')
clsmethod_pattern = re.compile('^([A-Za-z0-9А-Яа-я_]*).([A-zА-Яа-я]*)\(([^)]*)\)$')

# Input loop
while True:
    inp = input('> ')

    # Parse command and parameters
    inp = inp.strip()
    if not inp:
        continue
    parsed_inp = command_pattern.match(inp)
    if parsed_inp:
        command = parsed_inp.group(1)
        if command not in comHandler.commands:
            print('\nNo such function (write info() for functions list)\n')
            continue
        else:
            res = comHandler.handle(command, parsed_inp.group(2))

    else:
        parsed_inp = clsmethod_pattern.match(inp)
        if not parsed_inp:
            print('\nNot parsable command!\n')
            continue
        cls_name = parsed_inp.group(1)
        command = parsed_inp.group(2)
        arg = parsed_inp.group(3)
        if command not in comHandler.commands:
            print('\nNo such function (write info() for functions list)\n')
            continue
        else:
            res = comHandler.handle_cls(cls_name, command, arg)
    if res is not None:
        print(res + '\n')
