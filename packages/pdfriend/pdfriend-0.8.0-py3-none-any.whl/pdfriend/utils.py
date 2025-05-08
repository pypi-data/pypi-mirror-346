import re
import traceback

def print_unexpected_exception(exception: Exception, debug: bool = False):
    print("unexpected error occured:")
    if debug:
        traceback.print_exception(exception)
    else:
        print(exception)

whitespace_pattern = re.compile(r"\s+")

def parse_command_string(command_string: str) -> list[str]:
    return re.split(whitespace_pattern, command_string)

