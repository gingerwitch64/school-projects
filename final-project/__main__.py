# Before anything else, it should be stated the goals of this program:
# - To make changing of files easier to read. I don't forsee this program supporting changing of non-text files.
# - To have the entire program contained within a single file--no custom libraries, only libraries that are built into python.

a_definitely_useful_float_variable: float = 0.25
tutorial: list[str] = [] # Tutorial WILL be re-defined right before the program runs, but is removed from the top of the program to prevent clutter

# IMPORTED LIBRARIES
import sys, argparse, os # sys and argparse will be used to read command line arguments; os will be used for file operations
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
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S%z" # Year/Month/Day Hour:Minute:Second+-UTC offset ; to be used for patch files

# DATA TYPE VARIABLES
ADD,REM,MOD = "+","-","=" # The only reason I have decided to make these modular is because I may change the mod symbol later
ADD_FILE,REM_FILE,MOD_FILE = ADD*3,REM*3,MOD*3
ADD_ALT,REM_ALT,MOD_ALT = f"{ADD}ADDSYMBOL{ADD}",f"{REM}REMSYMBOL{REM}",f"{MOD}MODSYMBOL{MOD}"

class Change: # For changes per line
    type = None # Insertion, removal or other modification change?
    line = None
    condition = None
    text = str
    def __init__(self,type,line,text,condition = None):
        self.type = type
        self.text = text
        self.line = line
        self.condition = condition
    def __str__(self) -> str:
        type = str(self.type)
        swap = ""
        if   type == ADD:
            swap  =  ADD_ALT
        elif type == REM:
            swap  =  REM_ALT
        elif type == MOD:
            swap  =  MOD_ALT
        else:
            swap = type
        if self.condition != None:
            return f"{self.type}{self.line}{self.type}{str(self.text).replace(type,swap)}{str(self.type)*3}{self.condition.replace(type,swap)}\n"
        else:
            return f"{self.type}{self.line}{self.type}{str(self.text).replace(type,swap)}\n"
    __repr__ = __str__

class FileChange: # For changes per file
    type = None
    file = None
    changes = [] # The individual changes of the file
    def __init__(self,type,file,changes: list[Change]):
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
    desc = str
    date_time = datetime
    changes = list[FileChange]
    def __init__(self,name,date_time: datetime,changes: list[FileChange]):
        self.desc = name
        self.date_time = date_time
        self.changes = changes
    def __str__(self):
        start = f"@DESCRIPTION\n{self.desc}\n\n@DATETIME\n{self.date_time}\n\n"
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
                out_patch.desc = patchlines[patchlines.index(line)+1]
            elif line.strip("@") == "DATETIME":
                out_patch.date_time = datetime.strptime(patchlines[patchlines.index(line)+1],DATETIME_FORMAT)
    for line in patchlines:
        if line.startswith(ADD_FILE):
            f_change_buffer = FileChange(ADD_FILE,line.strip().strip(ADD_FILE),[])
            init_pos = patchlines.index(line)
            i = 1
            while True:
                if init_pos+i >= len(patchlines):
                    break
                current_line = patchlines[init_pos+i]
                if current_line.startswith(ADD_FILE): break
                elif current_line.strip().startswith("#"): pass
                elif current_line.startswith(ADD):
                    linedat = current_line.split(ADD,2)
                    f_change_buffer.changes.append(Change(ADD,int(linedat[1]),linedat[2].replace(ADD_ALT,ADD))) # With new files, line numbers MUST be specified.
                else: break
                i+=1
            out_patch.changes.append(f_change_buffer)
        elif line.startswith(MOD_FILE):
            f_change_buffer = FileChange(MOD_FILE,line.strip().strip(MOD_FILE),[])
            init_pos = patchlines.index(line)
            i = 1
            while True:
                if init_pos+i >= len(patchlines):
                    break
                current_line = patchlines[init_pos+i]
                if current_line.startswith(MOD_FILE): break
                elif current_line.strip().startswith("#"): pass
                elif current_line.startswith(MOD):
                    linedat = current_line.split(MOD,2)
                    if linedat[1].isdigit():
                        f_change_buffer.changes.append(Change(MOD,int(linedat[1]),linedat[2].replace(MOD_ALT,MOD)))
                    else:
                        chngdat_buffer = linedat[2].split(MOD_FILE)
                        f_change_buffer.changes.append(Change(MOD,linedat[1],chngdat_buffer[0].replace(MOD_ALT,MOD),chngdat_buffer[1].replace(MOD_ALT,MOD)))
                elif current_line.startswith(ADD):
                    linedat = current_line.split(ADD,2)
                    if linedat[1].isdigit():
                        f_change_buffer.changes.append(Change(ADD,int(linedat[1]),linedat[2].replace(ADD_ALT,ADD)))
                    else:
                        chngdat_buffer = linedat[2].split(ADD_FILE)
                        f_change_buffer.changes.append(Change(ADD,linedat[1],chngdat_buffer[0].replace(ADD_ALT,ADD),chngdat_buffer[1].replace(ADD_ALT,ADD)))
                elif current_line.startswith(REM):
                    linedat = current_line.split(REM,2)
                    if linedat[1].isdigit():
                        f_change_buffer.changes.append(Change(REM,int(linedat[1]),linedat[2].replace(REM_ALT,REM)))
                    else:
                        chngdat_buffer = linedat[2].split(REM_FILE)
                        f_change_buffer.changes.append(Change(REM,linedat[1],chngdat_buffer[0].replace(REM_ALT,REM),chngdat_buffer[1].replace(REM_ALT,REM)))
                else: break
                i+=1
            out_patch.changes.append(f_change_buffer)
        elif line.startswith(REM_FILE):
            out_patch.changes.append(FileChange(REM_FILE,line.strip(REM_FILE).replace(REM_ALT,REM),[]))
    return out_patch

def exec_patch(patch: ChangeLog, path: Path, log: bool = True):
    for filechange in patch.changes:
        if type(filechange) == FileChange:
            fpath = Path(path / filechange.file)
            if filechange.type == REM_FILE:
                if fpath.is_dir() and len(fpath.iterdir()) == 0:
                    fpath.rmdir()
                    if log: print(f"{fpath} removed.")
                elif fpath.is_dir() and len(fpath.iterdir()) != 0:
                    print(f"{ERR_PREFIX} The directory {fpath} still has files in it (cannot delete non-empty folder)")
                elif fpath.is_file():
                    fpath.unlink()
                    if log: print(f"{fpath} removed.")
                elif not fpath.exists():
                    if log: print(f"{fpath} ordered to be removed, but does not exist; ignoring.")
            if filechange.type == ADD_FILE:
                if filechange.changes == []:
                    if log: print(f"{fpath} being created as a directory (no changes; if you wanted to create a file, add at least \"+1+\")")
                    fpath.mkdir(parents=True,exist_ok=True)
                else:
                    if log: print(f"{fpath} being written...")
                    for change in filechange.changes:
                        


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
            "tutorial | tutor | t - Start a walkthrough on how to write a patchi file",
            "help | h - Prints this help text",
            "quit | exit | q - Exits this shell",
            "sysarg - Print arguments that were supplied to the program",
            "datetime | dt | d - Print datetime in patchi's format",
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
            elif command in {"tutorial","tutor","t"}:
                i = 0
                while i < len(tutorial):
                    print(i+1,tutorial[i])
                    input()
                    i+=1
            elif command == "sysarg":
                print(argv)
            elif command in {"datetime","dt","d"}:
                print(f"@DATETIME\n{datetime.now().astimezone().strftime(DATETIME_FORMAT)}")
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
                print("Unrecognized keyword.")
                for line in help_text: print(line)

# Here is the Tutorial, and where it is redefined.
tutorial = [
"(Press [ENTER] to print the next set of instructions.)",
"This tutorial will walk you through the essential parts of a patchi file.",
"""\
Firstly, it should be made clear the design of this format and program.
patchi intends to make reading and writing text patches intuitively and legibly,
without using a more complicated (although definitely superior) VCS such as git.\
""",
"""\
Two variables that should be included in every patchi file are:
 - @DESCRIPTION
 - @DATETIME

These provide useful metadate for the user and the program.

@DESCRIPTION will be the description of your patch.

@DATETIME will be automatically generated with an auto-generated patch,
but if you are manually writing a patch, you can copy-and-paste the
date-time that this program generates on startup or use "datetime" in-shell.

The description or datetime must be on the line AFTER the variable indicator.

Example:
@DESCRIPTION
My first patchi file!

@DATETIME
2023/05/31 23:00:00+0000\
""",
"""\
Comments in patchi are represented by "#"s.
Unlike other scripts and programming languages, comments MUST be on their own line.
Spacing before and after does not matter, however.

Example:
+++new.txt
 # This will make a new file!\
""",
"""\
Indicators in patchi include:
ADD (Insert): +
REM (Remove): -
MOD (Change): =

Indicators will separate the line number from the text to operate with.

File indicators will use three of either:
+++ indicates a brand new file
--- indicates deletion of a file
=== indicates modification of a file

Example:
+++new.txt
+4+Hello, world!
 # This will insert empty lines in a new file (in this case new.txt)
 # Until line 4, where "Hello, world!" will be inserted.
 # It should also be noted that all new files will be ended with a newline.

---deleteme.txt

===changeme.txt
=3=foo = True
 # This will replace the text on line three with "foo = True"
+4+bar = True
 # This will insert a new line with "bar = True", but move everything following it down.
 # Good for patches that are adding more to code.
-5-while True: pass
 # Similarly, this will remove a line but move all following lines upwards.\
""",
"There will be more to come!",
]

# Checks if python's version is greater than 3.4.x
# This is to ensure compatability with pathlib.
if (__name__ == "__main__") and (int(python_version().split(".")[0]) == v_req["major"]) and (int(python_version().split(".")[1]) >= v_req["minor"]) or (int(python_version().split(".")[0]) > v_req["major"]):
    main()
else:
    print(f"{ERR_PREFIX}: Python version must be at least {v_req['major']}.{v_req['minor']}")
    print(f"You python version is {python_version()}")
    # A quit statement is not needed here; if the program does not meet the version requirement, it will quit anyhow (End of File)
