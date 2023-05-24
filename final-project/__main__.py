import sys, pathlib, json
# sys will be used to read command line arguments.
from platform import python_version
from datetime import datetime

executed_from = pathlib.Path(__file__).parent.resolve()
err_prefix = "Error"
v = { # The version of this program
    "major": 0,
    "minor": 1,
    "patch": 0,
}
v_req = { # Python Version Requirements
    "major": 3,
    "minor": 10,
}

datetime_format = "%Y:%m:%d:%H:%M:%S"

default_indicators = {
    "same": "|",
    "add":  "+",
    "diff": "-",
    "comment": "&",
}

def parse_patch(filepath: type[str]):
    with open(filepath,"r") as f:
        for line in f:
            print(line)

def main():
    print(datetime.now().strftime(datetime_format))

# Checks if python's version is greater than 3.10.x
# This is to ensure compatability with match: case: statements.
if (__name__ == "__main__") and (python_version().split(".")[0] == str(v_req["major"]) and python_version().split(".")[1] >= str(v_req["minor"])) or (python_version().split(".")[0] > str(v_req["major"])):
    main()
else:
    print(f"{err_prefix}: Python version must be at least {v_req['major']}.{v_req['minor']}")
    # A quit statement is not needed here; if the program does not meet the version requirement, it will quit anyhow (End of File)
