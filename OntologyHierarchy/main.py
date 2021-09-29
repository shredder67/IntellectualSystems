# Program creates class hierarchy and instances, reads and saves it as JSON file.
# Allows to perform query throw the "knowledge base" of instances
# Instances have attributes of string, numerical and instance types
# Type info() for command information

# TODO:
#   find request to hierarchy

#   UPD1: check add_atr method for fix instructions, also add instance reading
#   UPD2: reading works greatly, need to add instance reading
#   UPD3: reworked Attribute instantiating, parsing works fine, need to test with instances



import signal
import sys
import re
from os import path
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
        'info': '() - prints all commands info',
        'create': '(hierarchy_name) - creates a new hiearchy and loads it in memory',
        'print': '() - prints the current hierarchy',
        'add_cls': '(name, super_class = None) - creates new class',
        'add_atr':  '(name, type) - adds attribute to class\ntype list:\n\tNUM_SINGLE - single number\n\t'
                    'NUM_MULTIPLE - number array\n\tSTR_SINGLE - single string\n\tSTR_MULTIPLE - string array'
                    'LINK_SINGLE - single link to other class/classes\n\tLINK_MULTIPLE - multiple links to other'
                    'class/classes',
        'inst': '({ atr_name : atr_value }) - creates an instance of class with entered parameters'
                'NOTE: use like this: cls_name.inst(args)',
        'print_inst': '() - prints all instances in hierarchy',
        'save': '(path) - saves hierarchy as json file',
        'open': '(path) - opens exiting hierarchy (from json)',
        'find': '(atr_name, condition) - searches through class and subclasses instances, applying condition to atr '
                'value '
    })
    commands = commands_desc.keys()

    # Handles function calls
    def handle(self, command_name, arg):
        mes = 'Nothing happened...'
        if command_name == 'info':
            mes = self._info()
        elif command_name == 'create':
            mes = self._create(arg)
        elif command_name == 'add_cls':
            mes = self._add_class(arg)
        elif command_name == 'print':
            mes = self._print()
        elif command_name == 'print_inst':
            mes = self._print_inst()
        elif command_name == 'save':
            mes = self._save(arg)
        elif command_name == 'open':
            mes = self._open(arg)
        return mes

    # Handles fuction calls related to classes in hierarchy in format cls_name.command(args)
    def handle_cls(self, cls_name, command_name, args):
        mes = 'Nothing happend...'

        cls = self.HierarchyObject.find_class(cls_name)
        if not cls:
            mes = 'No such class in hierarchy!'
            return mes

        if command_name == 'add_atr':
            mes = self._add_atr(cls, args)
        elif command_name == 'inst':
            mes = self._inst(cls, args)
        return mes

    def _info(self):
        for key in self.commands_desc:
            print(key + self.commands_desc[key])
        return ''

    def _create(self, arg):
        self.HierarchyObject = Hierarchy(arg)
        if (self.HierarchyObject):
            return 'Hierarchy created!'
        else:
            return 'Hierarchy wasn\'t created, smth went wrong'

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
        return 'Attribute ' + args[1] + ' added to ' + cls.name

    def _inst(self, cls, arg):
        # arg is value, value, value in defined order
        values = list(map(str.strip, arg.split(',')))
        cls.create_instance(values)
        return 'Instance created!'

    def _print(self):
        print('\n' + self.HierarchyObject.to_str())
        return ''

    def _print_inst(self):
        print(self.HierarchyObject.to_str(True))
        return ''

    def _save(self, arg):
        return ''

    def _open(self, arg):
        if path.exists(arg):
            self.HierarchyObject = Hierarchy()
            self.HierarchyObject.parse_from_json(arg)
            return 'Hierarchy parsed!'
        else:
            return 'Wrong path!'


# command(args)
# args : arg1, arg2, ..., argn or {... key : val ...}
comHandler = CommandHandler()
command_pattern = re.compile('^([A-z]*)\(([^)]*)\)$')
clsmethod_pattern = re.compile('^([A-Za-z0-9А-Яа-я]*).([A-zА-Яа-я]*)\(([^)]*)\)$')

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
        else:
            res = comHandler.handle(command, parsed_inp.group(2))
            print(res + '\n')
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
        else:
            res = comHandler.handle_cls(cls_name, command, arg)
            print(res + '\n')
