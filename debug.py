#!/usr/bin/env python

import os
import sys
import urllib.parse
from datetime import datetime

sys.path.append(os.path.dirname(__file__) + '/lib/python3.9/site-packages')
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/healthz')
def healthz():
    return 'healthy\n'

@app.route('/')
def index():
    x = [
      'Request Debugging Information',
      'Request time: %s' % datetime.now().isoformat(),
      'Please copy the contents of this web page and include it in your support requests',
      ''
    ]
    x.append("%s %s" % (request.method, request.url))
    x.append('')
    for a in request.headers:
        x.append("%s: %s" % (a[0], a[1]))
    x.append('')
    log = " -- ".join(x)
    data = request.get_data()
    if data:
        log += " ---- " + urllib.parse.quote_plus(data)
    sys.stderr.write(log + "\n")
    return Response(response="\n".join(x), status=404, mimetype="text/plain")

@app.errorhandler(404)
def not_found(error=None):
    return index()
		
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
