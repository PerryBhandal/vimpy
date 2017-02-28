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

    def echo(self, to_echo):
        vim.command(""":echo '%s' """ % to_echo)

    def _parse_args(self):
        return vim.eval("a:000")

    @property
    def buffer_file(self):
        return vim.current.buffer.name

vimpy = VimPy()
