from assembly_helpers import *

from collections import deque
from sys import argv

def assembler_interpreter(program, DEBUG=False):
    """Interprets lines of assembly program and returns a set return code"""

    # Tokenize the lines and filter out whitespace
    program = filter(None, map(process_line, program.split('\n')))

    # Convert to a tuple for indexing w/ the line counter
    program = tuple(program)

    # Error if no end statement in the program
    if all(line[0] != 'end' for line in program):
        return -1

    # Find all functions/routines for line jumping
    label_lines = {line[0].rstrip(':'): i for i, line in enumerate(program) if line[0][-1] == ':'}

    # Setting auxillary variables for the language
    memory = dict()
    registers, line_counter = dict(), 0
    prev_lines, return_code = deque(), str()
    while program[line_counter][0] != 'end':
        if DEBUG:
            print(program[line_counter], registers, memory, prev_lines, sep = '\n', end='\n\n')

        command, *other = program[line_counter]

        # mov command moves either a constant or register value to a register
        if command == 'mov':
            register, value = other
            registers[register] = get_value(value, registers)

        # inc increments the value of a register by 1
        elif command == 'inc':
            register = other[0]
            registers[register] += 1

        # dec decrements the value of a register by 1
        elif command == 'dec':
            register = other[0]
            registers[register] -= 1

        # add adds the contents of a register and a register or constant
        elif command == 'add':
            register, value = other
            registers[register] += get_value(value, registers)

        # sub subtracts the contents of a register and a register or constant
        elif command == 'sub':
            register, value = other
            registers[register] -= get_value(value, registers)

        # mul multiplies the contents of a register and a register or constant
        elif command == 'mul':
            register, value = other
            registers[register] *= get_value(value, registers)

        # div integer divides the contents of a register and a register or constant
        elif command == 'div':
            register, value = other
            registers[register] //= get_value(value, registers)

        # jmp jumps the line counter to the function/routine provided without storing the old location
        elif command == 'jmp':
            label = other[0]
            line_counter = label_lines[label]
        
        # call jumps the line counter to the function/routine provided while storing the previous one
        elif command == 'call':
            label = other[0]
            prev_lines.append(line_counter)
            line_counter = label_lines[label]

        # ret returns the line counter to the previous line before a routine was called
        elif command == 'ret':
            line_counter = prev_lines.pop()

        # cmp stores both values for the next jump comparison
        elif command == 'cmp':
            one, two = other
            compare = [get_value(one, registers),
                       get_value(two, registers)]

        # je jumps to function/routine if the comparison is ==
        elif command == 'je':
            label = other[0]
            if compare[0] == compare[1]:
                line_counter = label_lines[label]

        # ce call to function/routine if the comparison is ==
        elif command == 'ce':
            label = other[0]
            prev_lines.append(line_counter)
            if compare[0] == compare[1]:
                line_counter = label_lines[label]

        # jne jumps to function/routine if the comparison is !=
        elif command == 'jne':
            label = other[0]
            if compare[0] != compare[1]:
                line_counter = label_lines[label]

        # cne call to function/routine if the comparison is !=
        elif command == 'cne':
            label = other[0]
            prev_lines.append(line_counter)
            if compare[0] != compare[1]:
                line_counter = label_lines[label]

        # jge jumps to function/routine if the the comparison is >=
        elif command == 'jge':
            label = other[0]
            if compare[0] >= compare[1]:
                line_counter = label_lines[label]

        # cne call to function/routine if the comparison is >=
        elif command == 'cge':
            label = other[0]
            prev_lines.append(line_counter)
            if compare[0] >= compare[1]:
                line_counter = label_lines[label]

        # jg jumps to function/routine if the the comparison is >
        elif command == 'jg':
            label = other[0]
            if compare[0] > compare[1]:
                line_counter = label_lines[label]

        # cne call to function/routine if the comparison is >
        elif command == 'cg':
            label = other[0]
            prev_lines.append(line_counter)
            if compare[0] > compare[1]:
                line_counter = label_lines[label]

        # jle jumps to function/routine if the comparison is <=
        elif command == 'jle':
            label = other[0]
            if compare[0] <= compare[1]:
                line_counter = label_lines[label]

        # cne call to function/routine if the comparison is <=
        elif command == 'cle':
            label = other[0]
            prev_lines.append(line_counter)
            if compare[0] <= compare[1]:
                line_counter = label_lines[label]

        # jl jumps to function/routine if the comparison is <
        elif command == 'jl':
            label = other[0]
            if compare[0] < compare[1]:
                line_counter = label_lines[label]

        # cne call to function/routine if the comparison is <
        elif command == 'cl':
            label = other[0]
            prev_lines.append(line_counter)
            if compare[0] < compare[1]:
                line_counter = label_lines[label]

        # stw stores a value at a memory address
        elif command == 'stw':
            value, address = other
            address = get_address(address, registers)
            memory[address] = get_value(value, registers)

        # mvw takes a value from a memory address and stores it in a register
        elif command == 'mvw':
            register, address = other
            address = get_address(address, registers)
            registers[register] = memory[address]

        # msg stores the return output of the program
        elif command == 'msg':
            string = False
            for part in other:
                for character in part:
                    if character == "'":
                        string = not string
                    elif string:
                        return_code += character
                    elif character not in ', ':
                        return_code += str(registers[character])

        line_counter += 1

        # Catches programs that terminate incorrectly
        if line_counter >= len(program) or program[line_counter][-1] == ':':
            return -1

    return return_code

if __name__ == '__main__':
    if len(argv) < 2:
        print('Usage: assembly_interpreter.py file')

    DEBUG = False
    if len(argv) >= 3:
        DEBUG = argv[2] == '-d'

    assembly_file = argv[1]
    with open(assembly_file) as program:
        output = assembler_interpreter(program.read(), DEBUG)

    print(output)
