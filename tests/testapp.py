# -*- coding: utf-8 -*-
'''A simple flask app to use for testing.'''
import logging

from functools import wraps
from flask import Flask, Response, request, jsonify, redirect

logger = logging.getLogger(__name__)
app = Flask(__name__)


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

index_template = """<html>
    <head><title>This is the test app</title></head>
    <body>
        <a href="/foo/">Foo</a>
        <a href='/foo/bar/'>Bar</a>
    </body>
</html>
"""


@app.route("/")
def index():
    return index_template


@app.route("/foo/")
def foo():
    return ('<html><body>This is foo. <a href="./bar/">Bar</a> '
            '</body></html>')


@app.route("/foo/bar/")
@requires_auth
def bar():
    return '<html><body>This is bar.</body></html>'


@app.route("/foo/bar/baz/", methods=["POST", "PUT", "PATCH", "OPTIONS", "DELETE"])
@requires_auth
def baz():
    return jsonify({"secret": "myprecious"})


@app.route("/redirect/")
def r1():
    return redirect("/redirect2/")


@app.route("/redirect2/")
def r2():
    return redirect("/redirect3/")


@app.route("/redirect3/")
def r3():
    return jsonify({"status": "finished"})


@app.route("/secretjson/", methods=["POST"])
@requires_auth
def secretjson():
    logger.debug(request.content_type)
    return jsonify({"status": "finished"})


if __name__ == '__main__':
    app.run()
