# Before anything else, it should be stated the goals of this program:
# - To make changing of files easier to read. I don't forsee this program supporting changing of non-text files.
# - To have the entire program contained within a single file--no custom libraries, only libraries that are built into python.

# IMPORTED LIBRARIES
import sys, argparse # sys and argparse will be used to read command line arguments
from platform import python_version # make sure python is up to date enough to use certain libraries
from datetime import datetime # for change date/times
from pathlib import Path # to keep track of file/path location

# RUNTIME VARIABLES
# Variables with info on the conditions of the program's execution 
executed_from = Path(__file__).parent.resolve()
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--pass", "-p", action="store_true", help="Run the program without passing to the shell.")

# PROGRAM BEHAVIOR VARIABLES
v = { # The version of this program
    "major": 0,
    "minor": 1,
    "patch": 0,
}
v_req = { # Python Version Requirements
    "major": 3,
    "minor": 4,
}
ERR_PREFIX = "Error:"
DATETIME_FORMAT = "%Y/%m/%d %H:%M:%S %z %Z" # Year:Month:Day:Hour:Minute:Second ; to be used for patch files

# DATA TYPE VARIABLES
ADD,REM,MOD = "+","-","=" # The only reason I have decided to make these modular is because I may change the mod symbol later
ADD_FILE,REM_FILE,MOD_FILE = ADD*3,REM*3,MOD*3
ADD_ALT,REM_ALT,MOD_ALT = f"{ADD}ADDSYMBOL{ADD}",f"{REM}REMSYMBOL{REM}",f"{MOD}MODSYMBOL{MOD}"

class Change: # For changes per line
    type = None # Insertion, removal or other modification change?
    line = None
    text = str
    def __init__(self,type,line,text):
        self.type = type
        self.text = text
        self.line = line
    def __str__(self) -> str:
        type = str(self.type)
        swap = ""
        if type == ADD:
            swap = ADD_ALT
        elif type == REM:
            swap = REM_ALT
        elif type == MOD:
            swap = MOD_ALT
        else:
            swap = type
        return f"{self.type}{self.line}{self.type}{str(self.text).replace(type,swap)}\n"
    __repr__ = __str__

class FileChange: # For changes per file
    type = None
    file = None
    changes = [] # The individual changes of the file
    def __init__(self,type,file,changes):
        self.type = type
        self.file = file
        self.changes = changes
    def eval_path(self,path: Path):
        return path / self.file
    def __str__(self) -> str:
        start = f"{self.type}{self.file}\n"
        for change in self.changes:
            start += str(change)
        return start
    __repr__ = __str__

class ChangeLog: # For changes per patch
    name = None
    date_time = None
    changes = []
    def __init__(self,name,date_time,changes):
        self.name = name
        self.date_time = date_time
        self.changes = changes
    def __str__(self):
        start = f"@DESCRIPTION\n{self.name}\n\n@DATETIME\n{self.date_time}\n\n"
        for change in self.changes:
            start += str(change)
        return start
    __repr__ = __str__

def parse_patch(patch: str):
    out_patch = ChangeLog("",None,[])
    patchlines = patch.splitlines()
    for line in patchlines:
        if line.startswith("@"):
            if line.strip("@") == "DESCRIPTION":
                out_patch.name = patchlines[patchlines.index(line)+1]
            elif line.strip("@") == "DATETIME":
                out_patch.date_time = datetime.strptime(patchlines[patchlines.index(line)+1],DATETIME_FORMAT)
    for line in patchlines:
        if line.startswith(ADD_FILE):
            add_temp = FileChange(ADD_FILE,line.strip().strip(ADD_FILE),[])
            init_pos = patchlines.index(line)
            i = 1
            while True:
                if init_pos+i >= len(patchlines):
                    break
                current_line = patchlines[init_pos+i]
                if current_line.startswith(ADD_FILE): break
                elif current_line.startswith(ADD):
                    linedat = current_line.split(ADD,2)
                    add_temp.changes.append(Change(ADD,int(linedat[1]),linedat[2].replace(ADD_ALT,ADD)))
                else: break
                i+=1
            out_patch.changes.append(add_temp)
        elif line.startswith(REM_FILE):
            out_patch.changes.append(FileChange(REM_FILE,line.strip(REM_FILE).replace(REM_ALT,REM),[]))
    return out_patch

example_parsed = parse_patch("""@DESCRIPTION
A test with change types!

@DATETIME
2023/05/31 10:11:40 -0400 EDT

+++test.txt
+1+Hello!
+2+Woah!
+3+2+2=4
+4+""")
print(example_parsed)

def main(argv = sys.argv, args = arg_parser.parse_args()):
    print(f"patchi version {v['major']}.{v['minor']}.{v['patch']}")
    print(datetime.now().astimezone().strftime(DATETIME_FORMAT))
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
            "cd | changedir [directory] - Update the working directory",
            "ls | dir | listdir - List all files in the current path",
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
            elif command in {"cd","changedir"}:
                if len(given) == 1:
                    print(f"{ERR_PREFIX} Command requires 1 argument.")
                elif Path(path / given[1]).resolve().is_dir():
                    path = Path(path / given[1]).resolve()
                else:
                    print(f"{ERR_PREFIX} Directory \"{Path(path / given[1])}\" does not exist.")
            elif command in {"ls","dir","listdir"}:
                for dir in path.iterdir():
                    sdir = str(dir.resolve()).replace("\\","/").split("/")
                    print(sdir[len(sdir)-1])
            #elif command == "readpatch":
            #    if Path(path / given[1]).resolve().exists():
            #        parse_patch(Path(path / given[1]))
            #    else:
            #        print(f"{ERR_PREFIX} File \"{Path(path / given[1])}\" does not exist.")
            else:
                for line in help_text: print(line)

# Checks if python's version is greater than 3.4.x
# This is to ensure compatability with pathlib.
if (__name__ == "__main__") and (int(python_version().split(".")[0]) == v_req["major"]) and (int(python_version().split(".")[1]) >= v_req["minor"]) or (int(python_version().split(".")[0]) > v_req["major"]):
    main()
else:
    print(f"{ERR_PREFIX}: Python version must be at least {v_req['major']}.{v_req['minor']}")
    print(f"You python version is {python_version()}")
    # A quit statement is not needed here; if the program does not meet the version requirement, it will quit anyhow (End of File)
