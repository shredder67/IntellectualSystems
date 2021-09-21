# Program creates, stores, displays and allows ontology operations 
# on objects hierarchy. 

# TODO: 
# ! instance creation + print
# ! json parsing (with attributes), reading then saving
# ! find request to hierarchy

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
    hier = object()

    commands_desc = dict({
        'info':        '() - prints all commands info',
        'create':      '(hierarchy_name) - creates a new hiearchy and loads it in memory',
        'print':       '() - prints the current hierarchy',
        'add_cls':     '(name, super_class = None) - creates new class',
        'add_atr':     '(type (String, Num, Link), name, cardinality(single, multiple)(, cls_name if type is Link)) - adds attribute to class',
        'inst':        '({ atr_name : atr_value }) - creates an instance of class with entered parameters',
        'print_inst':  '() - prints all instances in hierarchy',
        'save':        '(path) - saves hierarchy as json file',
        'open':        '(path) - opens exiting hierarchy (from json)',
        'find':        '(atr_name, condition) - searches through class and subclasses instances, applying condition to atr value'
    })
    commands = commands_desc.keys()

    def handle(this, command_name, arg):
        mes = 'Nothing happend...'
        if command_name == 'info':
            mes = this._info()
        elif command_name == 'create':
            mes = this._create(arg)
        elif command_name == 'add_cls':
            mes = this._add_class(arg)
        elif command_name == 'print':
            mes = this._print()
        elif command_name == 'print_inst':
            mes = this._print_inst()
        elif command_name == 'save':
            mes = this._save(arg)
        elif command_name == 'open':
            mes = this._open(arg)
        return mes
    

    def handle_cls(this, cls_name, command_name, arg):
        mes = 'Nothing happend...'

        cls = this.hier.find_class(cls_name)
        if not cls:
            mes = 'No such class in hierarchy!'
            return mes

        if command_name == 'add_atr':
            mes = this._add_atr(cls, arg)
        elif command_name == 'inst':
            mes = this._inst(cls, arg)
        return mes
        
    
    def _info(this):
        for key in this.commands_desc:
            print(key + this.commands_desc[key])
        return ''


    def _create(this, arg):
        this.hier = Hierarchy(arg)
        if(this.hier):
            return 'Hierarchy created!'
        else:
            return 'Hierarchy wasn\'t created, smth went wrong'

    
    def _add_class(this, arg):
        args = arg.split(',')
        if(len(args) > 1):
            this.hier.add_class(args[0].strip(), args[1].strip())
        else:
            this.hier.add_class(args[0].strip())
        return 'Added class to hiearchy!'


    def _add_atr(this, cls, arg):
        args = list(map(str.strip, arg.split(',')))
        try:
            cls.add_atr(this, args[0], *args[1:])
        except IndexError:
            return 'Wrong amount of arguments!'
        except ValueError:
            return 'Wrong argument type!'
        return 'Attribute ' + args[1] + ' added to ' + cls.name


    def _inst(this, cls, arg):
        # arg is value, value, value in defined order
        values = list(map(str.strip, arg.split(',')))
        cls.create_instance(values)
        return 'Instance created!'

  
    def _print(this):
        print(this.hier.to_str())
        return ''

    def _print_inst(this):
        print(this.hier.to_str(True))
        return ''

    
    def _save(this, arg):
        pass

    
    def _open(this, arg):
        if path.exists(arg):
            this.hier.parse_from_json(arg)
            return 'Parsed hierarchy!'
        else:
            return 'Wrong path!'

# command(args)
# args : arg1, arg2, ..., argn or {... key : val ...}
comHandler = CommandHandler()
command_pattern = re.compile('^([A-z]*)\(([^)]*)\)$')
clsmethod_pattern = re.compile('^([A-Za-z0-9]*).([A-z]*)\(([^)]*)\)$')

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



