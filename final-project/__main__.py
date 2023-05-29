import sys, argparse, pathlib, json
# sys will be used to read command line arguments.
from platform import python_version
from datetime import datetime
from pathlib import Path

executed_from = Path(__file__).parent.resolve()

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--pass", "-p", action="store_true", help="Run the program without passing to the shell.")

err_prefix = "Error"
v = { # The version of this program
    "major": 0,
    "minor": 1,
    "patch": 0,
}
v_req = { # Python Version Requirements
    "major": 3,
    "minor": 4,
}

datetime_format = "%Y:%m:%d:%H:%M:%S" # Year:Month:Day:Hour:Minute:Second ; to be used for patch files

def parse_patch(filepath: type[Path]):
    with open(filepath,"r") as f:
        # "raw" line (untrimmed)
        for rline in f:
            line = rline.strip()
            print(line)
            if str(line).startswith("==="):
                testpath = filepath / str(line).removeprefix("===")
                print(testpath,testpath.exists(),testpath.is_dir())
                if not (testpath.exists() and testpath.is_dir()):
                    print("yay")

def write_patch(filepath: type[Path]):    
    pass

def main(argv = sys.argv, args = arg_parser.parse_args()):
    # This first statement is the shell. The program will redirect to here if no arguments are given.
    if len(argv) < 1 or (len(argv) < 2 and Path(argv[0]).resolve() == Path(__file__).resolve()):
        print("No arguments given, passing off to built-in shell:")
        shell = True
        path = executed_from
        help_text = [
            "",
            "patchi help menu",
            "help | h - Prints this help text",
            "quit | exit | q - Exits this shell",
            "sysarg - Print arguments that were supplied to the program",
            "readpatch - TESTING"
            "",
            ]
        while shell:
            given = input(f"{path}: ").split(" ")
            command = given[0]
            if command in {"quit","exit","q"}:
                print("Quitting")
                quit()
            elif command in {"help","h"}:
                for line in help_text: print(line)
            elif command == "sysarg":
                print(argv)
            elif command == "readpatch":
                parse_patch(Path("C:/Users/redpe/dev/school-projects/final-project/example.patch"))
            else:
                for line in help_text: print(line)
    print(f"patchi version {v['major']}.{v['minor']}.{v['patch']}")
    print(datetime.now().strftime(datetime_format))
    

# Checks if python's version is greater than 3.4.x
# This is to ensure compatability with pathlib.
if (__name__ == "__main__") and (int(python_version().split(".")[0]) == v_req["major"]) and (int(python_version().split(".")[1]) >= v_req["minor"]) or (int(python_version().split(".")[0]) > v_req["major"]):
    main()
else:
    print(f"{err_prefix}: Python version must be at least {v_req['major']}.{v_req['minor']}")
    print(f"You python version is {python_version()}")
    # A quit statement is not needed here; if the program does not meet the version requirement, it will quit anyhow (End of File)
