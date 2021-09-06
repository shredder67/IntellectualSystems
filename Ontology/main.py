# Program creates, stores, displays and allows ontology operations 
# on objects hierarchy. 
# Commands:
# create(hierarchy_name)
# print()
# add_class(name, super_class = None)
# add_atr(name, type, ...)
# add_obj(class, {atr : val})
# save(path)
# open(path)
# info()
import signal
import sys
import re
from hierarchy import Hierarchy

class mmodes:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def warning_print(mes):
        print(mmodes.BOLD + mmodes.UNDERLINE + mmodes.WARNING + mes + mmodes.ENDC)


def message_print(mes):
        print(mmodes.BOLD + mmodes.OKBLUE + mes + mmodes.ENDC)   


# Set up Ctrl-C handler for exiting program
def ctrl_c_handler(sig, frame):
    warning_print('Exiting...')
    sys.exit(0)

signal.signal(signal.SIGINT, ctrl_c_handler)

# Hierarchy object
hier = object()

# Static class, stores all commands and handle functions
class CommandHandler:
    commands_desc = dict({
        'info':         '(path) - prints all commands info',
        'create':       '(hierarchy_name) - creates a new hiearchy and loads it in memory',
        'print':        '() - prints the current hierarchy',
        'save':         '(path) - saves hierarchy as json file',
        'add_class':    '(name, super_class = None) - creates new class',
        'open':         '(path) - opens exiting hierarchy (from json)'
    })
    commands = commands_desc.keys()

    
    def handle(this, command_name, arg):
        mes = 'Nothing happend... Intersting!'
        if(command_name == 'info'):
            mes = this._info()
        elif(command_name == 'create'):
            mes = this._create(arg)
        elif(command_name == 'print'):
            print(hier)
            mes = "Finished printing!"
        elif(command_name == 'save'):
            mes = this._save(arg)
        elif(command_name == 'add_class'):
            mes = this._add_class(arg)
        elif(command_name == 'open'):
            mes = this._open(arg)
        return mes
        
    
    def _info(this):
        for name,desc in this.commands_desc.items():
            print(name + desc)
            return ''


    
    def _create(this, arg):
        global hier
        hier = Hierarchy(arg)
        if(hier):
            return 'Hierarchy created!'
        else:
            return 'Hierarchy wasn\'t created, smth went wrong'

    
    def _add_class(this, arg):
        global hier
        args = arg.split(',')
        if(len(args) > 1):
            hier.add_class(args[0].strip(), args[1].strip())
        else:
            hier.add_class(args[0].strip())
        return 'Added class to hiearchy!'

  
    def _print(this):
        hier.print()
        return ''

    
    def _save(this, arg):
        pass

    
    def _open(this, arg):
        pass

# command(args)
# args : arg1, arg2, ..., argn or {... key : val ...}
comHandler = CommandHandler()
command_pattern = re.compile('^([A-z]*)\(([^)]*)\)$')

# Input loop
while True:
    inp = input()

    # Parse command and parameters
    inp = inp.strip()
    if(not inp):
        continue
    parsed_inp = command_pattern.match(inp)
    if(not parsed_inp):
        warning_print('Non parsable command!')
        continue

    command = parsed_inp.group(1)
    if(command not in comHandler.commands):
        warning_print('No such funcion (write info() for functions list)')
    else:
        res = comHandler.handle(command, parsed_inp.group(2))
        message_print(res)

    
