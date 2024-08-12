import sys, os, pickle
from typing import Self, TextIO

# TODO NEXT LIVE : introduce parsig of list elements

class Line:
    def __init__(self : Self) -> None:    
        self.indentation_level : int = 0
        self.header : int = 0
        self.quatation : int = 0
        self.text : str = ""

lines : list[Line] = []

def main():
    arguments : list[str] = sys.argv[1:]

    if len(arguments) <= 3:
        print("\033[31;1mERROR : NOT ENOUGH ARGUMENTS (parser --help for help)", file=sys.stderr)
        exit(1)

    input_file : str = ""
    output_file : str = ""
    human_readable : bool = False

    if (not "-i" in arguments) or (not "-o" in arguments):
        print("\033[31;1mERROR : INPUT OR OUTPUT NOT SPECIFIED (parser --help for help)", file=sys.stderr)
        exit(2)

    input_file = arguments[arguments.index("-i") + 1]
    output_file = arguments[arguments.index("-o") + 1]

    if not os.path.exists(input_file):
        print("\033[31;1mERROR : INEXISTANT INPUT FILE (parser --help for help)", file=sys.stderr)
        exit(3)

    if not os.path.exists(output_file):
        try : temp_file : TextIO = open(output_file, "x")
        except :
            print("\033[31;1mERROR : FAILED TO CREATE OUTPUT FILE (parser --help for help)", file=sys.stderr)
            exit(4)
        else : temp_file.close()

    if "-r" in arguments : human_readable = True

    with open(input_file, "r") as input_buffer:
        for line in input_buffer.readlines():
            parse_line(line)
        save_lines_to_file(input_file, output_file, human_readable)

def find_line_begining_tokens(line : str, symbol : str, max_occurences : int) -> tuple[str, int]: #TODO : verify the minimal length
    for i in range(1, max_occurences+1):
        if line[:i+1] == (symbol * i + " "):
            return line[i+1:], i
    return line, 0

def reformat_middle_tokens(line : str, token_separator : str, replacement : str) -> str:
    tokens : list[str] = line.split(token_separator)
    if len(tokens) <= 1 or len(tokens) % 2 == 0:
        return line
    return_text : str = ""
    for i, token in enumerate(tokens):
        if i % 2:
            return_text += f"%[{replacement}]{token}%[/{replacement}]"
        else :
            return_text += token
    return return_text

def parse_line(line : str) -> None:
    global lines
    final_line_object : Line = Line()
    
    line, final_line_object.header = find_line_begining_tokens(line, "#", 6)
    line, final_line_object.quatation = find_line_begining_tokens(line, ">", 3)

    
    for char in line:
        if char == " ":
            line = line[1:]
            final_line_object.indentation_level += 1
        elif char == "\t":
            line = line[1:]
            final_line_object.indentation_level += 4
        else :
            break

    line = reformat_middle_tokens(line, "**", "bold")
    line = reformat_middle_tokens(line, "*", "italic")
    line = reformat_middle_tokens(line, "`", "code")
    
    final_line_object.text = line
    lines.append(final_line_object)

def save_lines_to_file(input_file : str, output_file : str, human_readable : bool):
    if human_readable:
        with open(output_file, "w") as output_buffer:
            for i, line in enumerate(lines):
                output_buffer.write(f"{i}: {line.text[:-1]} (header : {line.header}; quatation : {line.quatation}; indentation : {line.indentation_level})\n")
    else :
        with open(output_file, "wb") as output_buffer:
            pickle.dump(lines, output_buffer)

if __name__ == "__main__":
    main()
