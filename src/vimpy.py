import vim
import rc.debug as d
from rc.json import to_json

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
        else:
            print("ERROR: Action not found.")

vimpy = VimPy()
