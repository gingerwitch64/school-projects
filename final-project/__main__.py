# Before anything else, it should be stated the goals of this program:
# - To make changing of files easier to read. I don't forsee this program supporting changing of non-text files.
# - To have the entire program contained within a single file--no custom libraries, only libraries that are built into python.

tutorial: list[str] = [] # Tutorial WILL be re-defined right before the program runs, but is removed from the top of the program to prevent clutter

# IMPORTED LIBRARIES
import sys, argparse # sys and argparse will be used to read command line arguments
from platform import python_version # make sure python is up to date enough to use certain libraries
from datetime import datetime # for change date/times
from pathlib import Path # to keep track of file/path location
from time import time # to track function execution time

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
# Some line-function presets
FINDFIRSTLINE,FINDLASTLINE = "FINDFIRSTLINE","FINDLASTLINE"

class Change: # For changes per line
    type = None # Insertion, removal or other modification change?
    line = None # should either be a non-negative integer or a line-function
    condition = None # if the line number has a function, this will be text to find
    text = str # text to put on the line
    def __init__(self,type,line,text,condition = None): # class initialization (call when making a variable)
        self.type = type
        self.text = text
        self.line = line
        self.condition = condition
    def __str__(self) -> str:
        type = str(self.type)
        swap = "" # This makes sure that type symbols on same-type lines get replaced with alt-texts
        if type == ADD:
            swap  =  ADD_ALT
        elif type == REM:
            swap  =  REM_ALT
        elif type == MOD:
            swap  =  MOD_ALT
        else:
            swap = type
        if self.condition != None: # if there IS a condition (aka it is not none)
            # example: +FINDFIRSTLINE+print("Hello world!")+++print(2+ADDSYMBOL+2)
            return f"{self.type}{self.line}{self.type}{str(self.text).replace(type,swap)}{str(self.type)*3}{str(self.condition).replace(type,swap)}\n"
        else:
            # example: +1+print(2+ADDSYMBOL+2)
            return f"{self.type}{self.line}{self.type}{str(self.text).replace(type,swap)}\n"
    __repr__ = __str__

class FileChange: # For changes per file
    type = None # ADD, REM, MOD
    file = None # file name
    changes = [] # The individual changes of the file
    def __init__(self,type,file,changes: list[Change]):
        self.type = type
        self.file = file
        self.changes = changes
    def eval_path(self,path: Path): # helper function, currently unused
        return Path(path / self.file).resolve()
    def __str__(self) -> str:
        start = f"{self.type}{self.file}\n"
        for change in self.changes:
            start += str(change)
        # example:
        # +++new.txt
        # +1+Hello world!
        return start
    __repr__ = __str__

class ChangeLog: # For changes per patch
    desc = str # will be a description of a patch (like git's commit names)
    date_time = datetime # date and time (if someone is manually writing patches, you can get this when you start the program or through the shell)
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
    out_patch = ChangeLog("",None,[]) # Create a placeholder ChangeLog class
    patchlines = patch.splitlines() # go line by line through the patch file
    for line in patchlines:
        if line.startswith("@"):
            if line.strip("@") == "DESCRIPTION": # look for @DESCRIPTION, line after will be the description
                out_patch.desc = patchlines[patchlines.index(line)+1]
            elif line.strip("@") == "DATETIME": # look for @DATETIME, line after will be converted and used as the datetime
                out_patch.date_time = datetime.strptime(patchlines[patchlines.index(line)+1],DATETIME_FORMAT)
    for line in patchlines: # start going through again and look at actual changes
        if line.startswith(ADD_FILE):
            f_change_buffer = FileChange(ADD_FILE,line.strip().strip(ADD_FILE),[]) # the FileChange object buffer; when finished adding data, this will be appended to the overall ChangeLog
            init_pos = patchlines.index(line) # start parsing the individual line changes here
            i = 1 # offset from the start
            while True:
                if init_pos+i >= len(patchlines): # if the current line is the end of the file, stop looking (prevents out-of-bounds error)
                    break
                current_line = patchlines[init_pos+i] # get the current line
                if current_line.startswith(ADD_FILE): break # if the line starts with a +++, then it must not be a change under the current file
                elif current_line.strip().startswith("#"): pass # ignore comments (strip line so there is not whitespace messing it up)
                elif current_line.startswith(ADD):
                    linedat = current_line.split(ADD,2) # split by ONLY the first two characters, giving you the line number and the text
                    f_change_buffer.changes.append(Change(ADD,int(linedat[1]),linedat[2].replace(ADD_ALT,ADD))) # With new files, line numbers MUST be specified.
                else: break # FileChanges may be separated by empty lines and pretty much anything else, though not reccomended
                i+=1 # next line!
            out_patch.changes.append(f_change_buffer) # append the file change
        elif line.startswith(MOD_FILE):
            f_change_buffer = FileChange(MOD_FILE,line.strip().strip(MOD_FILE),[]) # buffer
            init_pos = patchlines.index(line) # start
            i = 1 # offset
            while True:
                if init_pos+i >= len(patchlines): # if EOF, stop
                    break
                current_line = patchlines[init_pos+i] # current line
                if current_line.startswith((MOD_FILE,ADD_FILE,REM_FILE)): break # MODified files need to cover all cases
                elif current_line.strip().startswith("#"): pass
                elif current_line.startswith(MOD): # all 3 of these different types are added the same way, so I will walk through the first:
                    linedat = current_line.split(MOD,2) # data from this line
                    if linedat[1].isdigit(): # if the line number (+NUM+) is an int, go ahead and just add the line
                        f_change_buffer.changes.append(Change(MOD,int(linedat[1]),linedat[2].replace(MOD_ALT,MOD)))
                    else: # if the line number is not an int, it must be a function; grab the condition
                        chngdat_buffer = linedat[2].split(MOD_FILE) # function arguments separated by ===
                        f_change_buffer.changes.append(Change(MOD,linedat[1],chngdat_buffer[0].replace(MOD_ALT,MOD),chngdat_buffer[1].replace(MOD_ALT,MOD))) # notice condition is added
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
                else: break # if anything irrelavent, break
                i+=1 # next
            out_patch.changes.append(f_change_buffer) # append the FileChange
        elif line.startswith(REM_FILE): # removing whole file, so no line changes needed
            out_patch.changes.append(FileChange(REM_FILE,line.strip(REM_FILE).replace(REM_ALT,REM),[]))
    return out_patch # return the ChangeLog with all of its data

def exec_patch(patch: ChangeLog, path: Path, log: bool = True): # log is used to print data, mainly for debugging but useful for end users
    start: float = time() # a float, which will be used to track how long it took this to run
    for filechange in patch.changes: # ChangeLog's changes are FileChange(s)
        if type(filechange) == FileChange: # mainly so editors like VSCode recognize object classes
            fpath = filechange.eval_path(path) # evaluate file location
            if filechange.type == REM_FILE:
                if fpath.is_dir() and len(fpath.iterdir()) == 0: # check if dir is empty
                    fpath.rmdir()
                    if log: print(f"{fpath} removed.")
                elif fpath.is_dir() and len(fpath.iterdir()) != 0: # if dir is not empty, simply skip it
                    print(f"{ERR_PREFIX} The directory {fpath} still has files in it (cannot delete non-empty folder)")
                elif fpath.is_file(): # if file, then remove
                    fpath.unlink()
                    if log: print(f"{fpath} removed.")
                elif not fpath.exists(): # if non-existent, ignore but log it
                    if log: print(f"{fpath} ordered to be removed, but does not exist; ignoring.")
            elif filechange.type == ADD_FILE:
                if filechange.changes == []: # explained by print statement under this comment
                    if log: print(f"{fpath} being created as a directory (no changes; if you wanted to create a file, add at least \"+1+\")")
                    fpath.mkdir(parents=True,exist_ok=True) # create any directories inbetween, okay if it already exists
                else: # if there are changes, will be a file
                    if log: print(f"{fpath} being written...")
                    lines = []
                    for change in filechange.changes:
                        if type(change) == Change:
                            if str(change.line).isdigit(): # make sure that this is not a function, not that it should be
                                if int(change.line) > len(lines): # if the line is out of bounds of the current lines length,
                                    while len(lines) < int(change.line)-1: lines.append("") # add more lines
                                if int(change.line) <= len(lines):
                                    lines.pop(int(change.line)) # pop line before adding
                                lines.insert(int(change.line)-1,str(change.text)) # now insert line
                    with open(fpath,mode="w+") as file:
                        file.write('\n'.join(lines)) # write lines
            elif filechange.type == MOD_FILE:
                lines = [i.rstrip('\n') for i in open(fpath).readlines()] # because reading from an existing file, make sure to strip newlines
                for change in filechange.changes:
                    if type(change) == Change:
                        if str(change.line).isdigit(): change.line = int(change.line) # if digit, make it a digit
                        elif str(change.line).isdigit() == False: # if not a digit, evaluate function
                            try:
                                if change.line == FINDFIRSTLINE: change.line = lines.index(str(change.condition))
                                # FINDLASTLINE: reverse the list, find the index, then subtract from line length to get the normal index
                                elif change.line == FINDLASTLINE: change.line = len(lines) - [lines[i] for i in range(len(lines)-1,-1,-1)].index(change.condition)
                            except ValueError: # .index() returns ValueError if no matches are found
                                print(f"{ERR_PREFIX} {change.condition} was not found on any line; {change.type} operation to \"{change.text}\" will not be made.")
                                continue # skip this change
                        if change.type == ADD: # direct insertion: no lines changed
                            if int(change.line) > len(lines):
                                while len(lines) < int(change.line)-1: lines.append("")
                            lines.insert(int(change.line)-1,str(change.text))
                        elif change.type == REM: # delete line
                            lines.pop(int(change.line))
                        elif change.type == MOD: # replacement, remove one line and put in another
                            if int(change.line) > len(lines):
                                while len(lines) < int(change.line)-1: lines.append("")
                            lines[int(change.line)-1] = change.text # replace text
                with open(fpath,mode="w+") as file: # open as write and create, just in case it doesn't exist
                    file.write('\n'.join(lines)) # join lines by a newline (removed in the beginning)
    end: float = time() # get the finishing time
    if log: print("Change execution completed in",end-start,"seconds.") # print time difference

def main(argv = sys.argv, args = arg_parser.parse_args()):
    print(f"patchi version {v['major']}.{v['minor']}.{v['patch']}")
    print(datetime.now().astimezone().strftime(DATETIME_FORMAT))
    if len(argv) < 1 or (len(argv) < 2 and Path(argv[0]).resolve() == Path(__file__).resolve()): # This first statement is the shell. The program will redirect to here if no arguments are given.
        print("No arguments given, passing off to built-in shell:")
        shell = True # while loop variable
        path = executed_from # starting path
        help_text = [
            "",
            "patchi help menu",
            "tutorial | tutor | t - Start a walkthrough on how to write a patchi file",
            "help | h - Prints this help text",
            "quit | exit | q - Exits this shell",
            "apply | execute [patchi file] - Parse and execute a patch file",
            "    NOTE: Make sure you are in the directory that you want the patch to be executed in.",
            "sysarg - Print arguments that were supplied to the program",
            "datetime | dt | d - Print datetime in patchi's format",
            "cd | changedir [directory] - Update the working directory",
            "ls | dir | listdir - List all files in the current path",
            "",
            ]
        while shell:
            # output patchi x.y.z, /current/path: and get the argument(s) following
            given = input(f"patchi {v['major']}.{v['minor']}.{v['patch']}\n{path}: ").split(" ")
            command = given[0] # for ease of coding, also makes sense intuitively because then given[1] will be your first arg
            if command in {"quit","exit","q"}: # checks if command is any one of these
                print("Quitting")
                quit(0) # quits with code 0 (success on most operating systems)
            elif command in {"help","h"}:
                for line in help_text: print(line)
            elif command in {"tutorial","tutor","t"}: # tutorial text
                i = 0
                while i < len(tutorial):
                    print(i+1,tutorial[i])
                    inpt = input() # will continue to next line upon [ENTER]
                    if inpt in {"quit","exit","q","end","stop"}: break # break quits while loop
                    i+=1 # next piece
            elif command == "sysarg":
                print(argv) # system arguments
            elif command in {"apply","execute","exec"}:
                exec_patch(
                    parse_patch(Path(path / given[1])
                                .resolve() # simplify/system-specify path
                                .open() # open file
                                .read() # read the plain text, DON'T split by lines
                    ),
                    path # from where changes will be executed
                )
            elif command in {"datetime","dt","d"}: # patchi compatable datetime generation
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
                    sdir = str(dir.resolve()).replace("\\","/").split("/") # split file path
                    print(sdir[len(sdir)-1]) # get last part of file path (will be the file name)
            else:
                print(f"Unrecognized keyword: \"{command}\"")
                for line in help_text: print(line)

# Here is the Tutorial, and where it is redefined.
tutorial = [
"(Press [ENTER] to print the next set of instructions, stop or end to quit.)",
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

Also note that +++ can be used to create a directory if you don't specify any changes,
and --- can be used to delete (empty) directories and files.

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
"""\
Alt-text are used in place of the +, -, and = symbols to allow the program to parse correctly.

Alt-texts are not required when a line number is present.

Alt-texts are:
+ADDSYMBOL+ for +
-REMSYMBOL- for -
=MODSYMBOL= for =\
""",
"""\
patchi has its own form of functions.
As of now there are two: FINDFIRSTLINE and FINDLASTLINE.
The syntax for these functions are as follows:
=FUNCTION=text_to_use===text_to_replace

For example, the line =FINDFIRSTLINE=me=MODSYMBOL=True===me=MODSYMBOL=False
would change the first occurance of the line:
me=False
to:
me=True

Alt-texts MUST be used when a function is included in a line, but you only need to use alt-texts if your operation uses a corresponding symbol.\
""",
"""\
Finally, here is an example of a patch file:

@DESCRIPTION
My first patchi file!

@DATETIME
2023/05/31 23:00:00+0000

+++addme.txt
+1+yay :)

+++newdir

---removeme.txt

---emptydir
 # patchi will automatically evaluate whether or not a path is a directory or file.

===changeme.txt
=FINDLASTLINE=me=MODSYMBOL=True===me=MODSYMBOL=False\
"""
"""\
As is the goal of patchi, this patchfile is clean, legible and consise.\
"""
"That's all for now!",
]

# Checks if python's version is greater than 3.4.x
# This is to ensure compatability with pathlib.
if (__name__ == "__main__") and (
int(python_version().split(".")[0]) == v_req["major"]) and (int(python_version().split(".")[1]) >= v_req["minor"] # is version 3.x?
) or (
int(python_version().split(".")[0]) > v_req["major"]): # is the version major >3?
    main()
else:
    print(f"{ERR_PREFIX}: Python version must be at least {v_req['major']}.{v_req['minor']}")
    print(f"Your python version is {python_version()}")
    # A quit statement is not needed here; if the program does not meet the version requirement, it will quit anyhow (End of File)
