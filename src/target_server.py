from flask import Flask, request
from rc.json import to_json, from_json
app = Flask(__name__)
import pprint
import json

@app.route("/", methods=["POST"])
def root():
    payload = request.data
    print(payload)
    return payload

app.run(debug=True, port=5000)
