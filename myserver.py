#!/usr/bin/env python
import subprocess
from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['POST'])
def ping():
    print "ping"

    process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
    output = process.communicate()[0]

    print output

    return "ok"


application = app # For WSGI

if __name__ == '__main__':
    app.run('0.0.0.0', 4567, use_reloader=True)
