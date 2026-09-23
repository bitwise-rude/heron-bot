'''
    Written by: Meyan Adhikari

    Contains all the necessary functions heron might need.

    Every function must have a docstring explaining its use case
    -- means it will be shown while the /help command is issued showing
    the total list of commands that can be used.
'''
from datetime import datetime


def get_now():
    '''
      Get-Time: Get the current system time.
    '''
    now = datetime.now()
    return str(now)

def get_all_commands():
    '''
        Show-All: Get all the commands 
    '''
    all_info = "\n".join([func.__doc__ for func in all_commands])

    return all_info

all_commands = [get_now, get_all_commands]
