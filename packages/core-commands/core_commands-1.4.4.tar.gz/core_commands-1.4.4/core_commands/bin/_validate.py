from .command_list_cmd import cmd_commands

def _validateArguments(arguments):
    if arguments == "None":
        return False
    if arguments == None:
        return False
    return True

def _validateCommand(command):
    for _command in cmd_commands:
        if command == _command:
            return True
        return False
    
