def get_address(address, registers):
    """Gets the numerical address from the possible access modes allowed"""
    
    try:
        address, offset = address.split('+')
        offset = int(offset)
    except ValueError:
        try:
            address, offset = address.split('-')
            offset = -int(offset)
        except ValueError:
            offset = 0

    if address.isdigit():
        return int(address)

    return int(registers[address]) + offset

def get_value(value: str, registers: dict):
    """Returns a constant if value is an integer or the register value otherwise"""

    if value in registers:
        return registers[value]

    return int(value)

def process_line(line: str):
    """Removes comments and unneeded whitespace. Returns a split list of
    instructions/registers"""
    
    comment_start = line.find(';')

    # Remove comments, one comment per line allowed
    if comment_start != -1:
        line = line[:comment_start]

    line = line.strip()
    
    # Splits commands such that the command and all details are seperated
    # "command ..." -> [command, ...]
    try:
        command, contents = line.split(maxsplit = 1)
    # Deals with function names, two special commands, and empty lines
    except ValueError:
        if line == '':
            return None
        elif line[-1] == ':' or line == 'end' or line == 'ret':
            return (line,)

    # Splits depending on command type, some requiring one argument, others two
    try:
        one, two = contents.split(',')
        return command, one.strip(), two.strip()
    except ValueError:
        return command, contents.strip()
