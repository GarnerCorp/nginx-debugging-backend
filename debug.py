#!/usr/bin/env python

import os
import http
import sys
import urllib.parse
from datetime import datetime

sys.path.append(os.path.dirname(__file__) + '/lib/python3.9/site-packages')
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/healthz')
def healthz():
    return 'healthy\n'

@app.route('/429', methods=['GET', 'POST'])
def too_many_requests():
    headers = {
        'Retry-After': 30
    }
    response = [
        '<title>Too many requests</title>',
        '<h1>Too many requests</h1>',
        '<strong>429.</strong> That’s an error.'
        '<p>',
        'We’re sorry but you have sent too many requests to us recently.',
        '</p>',
        '<p>Please try again later.',
        '<em>That’s all we know.</em>',
        '</p>',
        ''
    ]
    x = [
        'Too many requests',
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
    return Response(
        status=http.HTTPStatus.TOO_MANY_REQUESTS,
        headers=headers,
        response="\n".join(response),
        mimetype="text/html",
    )

def special_responses():
    code = request.headers['X-Code']
    if code == "429":
        return too_many_requests()
    if code == "503":
        return too_many_requests()
    code_str = str(code)
    try:
        kind = http.HTTPStatus(code)
    except ValueError:
        kind = "HTTP Error " + code_str

    response = [
        '<title>' + kind + '</title>',
        '<h1>' + kind + '</h1>',
        '<strong>' + code_str + '</strong> That’s an error.'
        '<p>',
        'We’re sorry.',
        '</p>',
        '<p>Please try again later.',
        '<em>That’s all we know.</em>',
        '</p>',
        ''
    ]
    x = [
        kind,
        ''
    ]
    x.append("%s %s" % (request.method, request.url))
    x.append('')
    for a in request.headers:
        x.append("%s: %s" % (a[0], a[1]))
    log = " -- ".join(x)
    data = request.get_data()
    if data:
        log += " ---- " + urllib.parse.quote_plus(data)
    sys.stderr.write(log + "\n")
    return Response(response="\n".join(x), status=code, mimetype="text/html")

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'X-Code' in request.headers:
        return special_responses()
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
    return Response(response="\n".join(x), status=http.HTTPStatus.NOT_FOUND, mimetype="text/plain")

@app.errorhandler(404)
def not_found(error=None):
    return index()
		
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
