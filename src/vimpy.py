import vim, re
import rc.debug as d
from rc.json import to_json

class Events(object):

    BUF_NEW_FILE = "BufNewFile"

    BUF_READ_PRE = "BufReadPre"

    BUF_READ = "BufRead"

    BUF_READ_POST = "BufReadPost"

    BUF_READ_CMD = "BufReadCmd"

    FILE_READ_PRE = "FileReadPre"

    FILE_READ_POST = "FileReadPost"

    FILE_READ_CMD = "FileReadCmd"

    FILTER_READ_PRE = "FilterReadPre"

    FILTER_READ_POST = "FilterReadPost"

    STDIN_READ_PRE = "StdinReadPre"

    STDIN_READ_POST = "StdinReadPost"

    BUF_WRITE = "BufWrite"

    BUF_WRITE_PRE = "BufWritePre"

    BUF_WRITE_POST = "BufWritePost"

    BUF_WRITE_CMD = "BufWriteCmd"

    FILE_WRITE_PRE = "FileWritePre"

    FILE_WRITE_POST = "FileWritePost"

    FILE_WRITE_CMD = "FileWriteCmd"

    FILE_APPEND_PRE = "FileAppendPre"

    FILE_APPEND_POST = "FileAppendPost"

    FILE_APPEND_CMD = "FileAppendCmd"

    FILTER_WRITE_PRE = "FilterWritePre"

    FILTER_WRITE_POST = "FilterWritePost"

    BUF_ADD = "BufAdd"

    BUF_CREATE = "BufCreate"

    BUF_DELETE = "BufDelete"

    BUF_WIPEOUT = "BufWipeout"

    BUF_FILE_PRE = "BufFilePre"

    BUF_FILE_POST = "BufFilePost"

    BUF_ENTER = "BufEnter"

    BUF_LEAVE = "BufLeave"

    BUF_WIN_ENTER = "BufWinEnter"

    BUF_WIN_LEAVE = "BufWinLeave"

    BUF_UNLOAD = "BufUnload"

    BUF_HIDDEN = "BufHidden"

    BUF_NEW = "BufNew"

    SWAP_EXISTS = "SwapExists"

    FILE_TYPE = "FileType"

    SYNTAX = "Syntax"

    ENCODING_CHANGED = "EncodingChanged"

    TERM_CHANGED = "TermChanged"

    VIM_ENTER = "VimEnter"

    GUI_ENTER = "GUIEnter"

    TERM_RESPONSE = "TermResponse"

    VIM_LEAVE_PRE = "VimLeavePre"

    VIM_LEAVE = "VimLeave"

    FILE_CHANGED_SHELL = "FileChangedShell"

    FILE_CHANGED_SHELL_POST = "FileChangedShellPost"

    FILE_CHANGED_RO = "FileChangedRO"

    SHELL_CMD_POST = "ShellCmdPost"

    SHELL_FILTER_POST = "ShellFilterPost"

    FUNC_UNDEFINED = "FuncUndefined"

    SPELL_FILE_MISSING = "SpellFileMissing"

    SOURCE_PRE = "SourcePre"

    SOURCE_CMD = "SourceCmd"

    VIM_RESIZED = "VimResized"

    FOCUS_GAINED = "FocusGained"

    FOCUS_LOST = "FocusLost"

    CURSOR_HOLD = "CursorHold"

    CURSOR_HOLD_I = "CursorHoldI"

    CURSOR_MOVED = "CursorMoved"

    CURSOR_MOVED_I = "CursorMovedI"

    WIN_ENTER = "WinEnter"

    WIN_LEAVE = "WinLeave"

    TAB_ENTER = "TabEnter"

    TAB_LEAVE = "TabLeave"

    CMDWIN_ENTER = "CmdwinEnter"

    CMDWIN_LEAVE = "CmdwinLeave"

    INSERT_ENTER = "InsertEnter"

    INSERT_CHANGE = "InsertChange"

    INSERT_LEAVE = "InsertLeave"

    COLOR_SCHEME = "ColorScheme"

    REMOTE_REPLY = "RemoteReply"

    QUICK_FIX_CMD_PRE = "QuickFixCmdPre"

    QUICK_FIX_CMD_POST = "QuickFixCmdPost"

    SESSION_LOAD_POST = "SessionLoadPost"

    MENU_POPUP = "MenuPopup"

    USER = "User"

class Cursor(object):

    def __init__(self):
        result = vim.eval("""getpos(".")""")
        assert len(result) == 4

        self.row = int(result[1])
        self.col = int(result[2])

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
        code = open(self.buffer_file, "r").readlines()
        line = code[self.cursor.row-1]
        return line

    def run_action(self):
        action_name = self.args[0]

        if action_name == "print_lines":
            print(self.line)
        elif action_name == "register_events":
            for event in VIM_EVENTS:
                vim.command(""":autocmd %s * :call RCFunc("event_fired", "%s")""" % (event, event))
        elif action_name == "event_fired":
            with open("/home/perry/dump.txt", "w+") as f:
                f.write("Event fired: %s\n" % self.args[1])
        else:
            print("ERROR: Action not found.")

vimpy = VimPy()
