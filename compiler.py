import sys, os, pickle
from parser import Line

def main():
    arguments : list[str] = sys.argv[1:]

    if len(arguments) <= 3:
        print("\033[31;1mERROR : NOT ENOUGH ARGUMENTS (copiler --help for help)", file=sys.stderr)
        exit(1)

    input_file : str = ""
    output_file : str = ""
    human_readable : bool = False

    if (not "-i" in arguments) or (not "-o" in arguments):
        print("\033[31;1mERROR : INPUT OR OUTPUT NOT SPECIFIED (compiler --help for help)", file=sys.stderr)
        exit(2)

    input_file = arguments[arguments.index("-i") + 1]
    output_file = arguments[arguments.index("-o") + 1]

    if not os.path.exists(input_file):
        print("\033[31;1mERROR : INEXISTANT INPUT FILE (compiler --help for help)", file=sys.stderr)
        exit(3)

    if not os.path.exists(output_file):
        try : temp_file : TextIO = open(output_file, "x")
        except :
            print("\033[31;1mERROR : FAILED TO CREATE OUTPUT FILE (compiler --help for help)", file=sys.stderr)
            exit(4)
        else : temp_file.close()
    
    clear_file(output_file)
    save_line_to_file("<link href=\"./default_theme.css\" type=\"text/css\" rel=\"stylesheet\"/>", output_file)
    save_line_to_file("<div class=\"generated-page\">", output_file)
    with open(input_file, "rb") as input_file:
        lines = pickle.load(input_file)
        for line in lines:
            save_line_to_file(compile_line(line), output_file)
    save_line_to_file("</div>", output_file)

def in_tag_text(text : str, tag : str) -> str:
    return f"<{tag}>{text}</{tag}>"

def compile_line(line : Line) -> str: # TODO : support escaping the tags
    final_line : str = ""
    final_line = line.text.replace("%[code]", "<code>")
    final_line = final_line.replace("%[/code]", "</code>")
    final_line = final_line.replace("%[italic]", "<em>")
    final_line = final_line.replace("%[/italic]", "</em>")
    final_line = final_line.replace("%[bold]", "<strong>")
    final_line = final_line.replace("%[/bold]", "</strong>")

    if line.quatation:
        for i in range(line.quatation):
            final_line = in_tag_text(final_line[:-1], "blockquote")
            final_line += "\n"
    if line.header:
        final_line = in_tag_text(final_line[:-1], f"h{line.header}")
        final_line += "\n"
    
    return final_line

def clear_file(file : str):
    with open(file, "w") as clear:
        clear.write("")

def save_line_to_file(line : str, file : str):
    with open(file, "a") as output_file:
        output_file.write(line)

if __name__ == "__main__":
    main()
