import vim

class Cursor(object):

    def __init__(self):
        result = vim.eval("""getpos(".")""")
        assert len(result) == 4

        self.row = int(result[1])
        self.col = int(result[2])

class VimPy(object):

    def __init__(self):
        self.cursor = Cursor()

    def echo(self, to_echo):
        vim.command(""":echo '%s' """ % to_echo)

    def get_args(self):
        result = vim.eval("a:000")

vimpy = VimPy()
