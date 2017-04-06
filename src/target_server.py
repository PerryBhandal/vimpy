from flask import Flask, request
from rc.json import to_json, from_json, Serializable
app = Flask(__name__)
import pprint
import json
import rc.debug.cpy as d

class ActionBase(object):

    def execute(self):
        raise NotImplementedError("Must override execute")

class Cursor(object):

    def __init__(self, row: int, col:int):
        self.row = row
        self.col = col

class AutoCompl(object):

    def __init__(self, cursor: str, buffer_name):
        self.cursor = cursor # type: Cursor
        self.buffer_name = buffer_name

    def execute(self):
        file_code = open(self.buffer_name, "r").readlines()
        cur_line = file_code[self.cursor.row-1]
        print("Code is %s" % cur_line)

Serializable.add_classes([Cursor, AutoCompl])

@app.route("/", methods=["POST"])
def root():
    payload = request.data

    dmp = payload.decode("utf-8")

    js_object = from_json(dmp)
    js_object.execute()
    return payload

app.run(debug=True, port=5000)
