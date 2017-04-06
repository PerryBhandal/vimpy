import sys
sys.path.append("/home/perry/work/git/rclib/src/")
import vim, re
import rc.debug as d
from rc.json import to_json
import requests

TO_GEN = """BufNewFile
BufReadPre
BufRead
BufReadPost
BufReadCmd
FileReadPre
FileReadPost
FileReadCmd
FilterReadPre
FilterReadPost
StdinReadPre
StdinReadPost
BufWrite
BufWritePre
BufWritePost
BufWriteCmd
FileWritePre
FileWritePost
FileWriteCmd
FileAppendPre
FileAppendPost
FileAppendCmd
FilterWritePre
FilterWritePost
BufAdd
BufCreate
BufDelete
BufWipeout
BufFilePre
BufFilePost
BufEnter
BufLeave
BufWinEnter
BufWinLeave
BufUnload
BufHidden
BufNew
SwapExists
FileType
Syntax
EncodingChanged
TermChanged
VimEnter
GUIEnter
TermResponse
VimLeavePre
VimLeave
FileChangedShell
FileChangedShellPost
FileChangedRO
ShellCmdPost
ShellFilterPost
FuncUndefined
SpellFileMissing
SourcePre
SourceCmd
VimResized
FocusGained
FocusLost
CursorHold
CursorHoldI
CursorMoved
CursorMovedI
WinEnter
WinLeave
TabEnter
TabLeave
CmdwinEnter
CmdwinLeave
InsertEnter
InsertChange
InsertLeave
ColorScheme
RemoteReply
QuickFixCmdPre
QuickFixCmdPost
SessionLoadPost
MenuPopup
User"""

TO_GEN = """CursorMoved
CursorHold
CursorHoldI
CursorMovedI"""


VIM_EVENTS = TO_GEN.split("\n")

class Cursor(object):

    def __init__(self):
        result = vim.eval("""getpos(".")""")
        assert len(result) == 4

        self.row = int(result[1])
        self.col = int(result[2])

class AsyncRequest(object):

    def send(self):
        requests.post("http://localhost:5000", data = to_json(self))

    def get_data(self):
        raise RuntimeError("Must override get data")

class AutoCompl(AsyncRequest):

    def __init__(self, cursor, buffer_name):
        self.cursor = cursor
        self.buffer_name = buffer_name

class VimPy(object):

    def __init__(self):
        self.cursor = Cursor()
        self.args = self._parse_args()
        self.run_action()

    def echo(self, to_echo):
        vim.command(""":echo '%s' """ % to_echo)

    def _parse_args(self):
        return vim.eval("a:000")

    @property
    def buffer_file(self):
        return vim.current.buffer.name

    @property
    def line(self):
        buffer_name = self.buffer_file
        if "vimpy.py" not in buffer_name:
            code = open(buffer_name, "r").readlines()
            line = code[self.cursor.row-1]
            return line
        else:
            print("ERROR: Tried to run a command on vimpy.py")

    def run_action(self):
        action_name = self.args[0]

        class SomeObject(object):

            def __init__(self, name):
                self.name = name

        if action_name == "print_lines":
            #print("Line is %s" % self.line)
            pass
        elif action_name == "auto_complete":
            line_data = self.line
            curs = Cursor()
            AutoCompl(curs, self.buffer_file).send()

            #print("%s:%s" % (curs.row, curs.col))
            sliced = line_data[curs.col-1:-1]
            #print(sliced)

        elif action_name == "register_events":
            for event in VIM_EVENTS:
                vim.command(""":autocmd %s * :call RCFunc("event_fired", "%s")""" % (event, event))
        elif action_name == "event_fired":
            with open("/home/perry/go.txt", "a") as f:
                f.write("Event fired\n")
            #vim.command(""":!echo %s >> /home/perry/go.txt""" % self.args[1])
        else:
            print("ERROR: Action not found.")

vimpy = VimPy()
