from bottle import run, post, get, response, route, static_file, delete, HTTPResponse
import json
import os
import sys


class InputContainer(object):

    inputsList = []

    def define_inputs_state(self):
        del self.inputsList[:]
        for item in context.get_inputs():
            self.inputsList.append(item)
        return


inputList = InputContainer()


# create doors
@get('/inputs')
def get_inputs():
    inputList.define_inputs_state()
    response.set_header('Access-Control-Allow-Origin', '*')
    response.add_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS, DELETE')
    response.headers['Content-Type'] = 'text/html'
    response.headers['Cache-Control'] = 'no-cache'
    output = []
    for item in inputList.inputsList:
        output.append({"id" : item.id,  "inputNumber": item.inputNumber, "moduleName": item.moduleName,
        "name": item.name, "status": str(item.status)})
    return json.dumps(output)

@get("/<filepath:re:.*\.css>")
def css(filepath):
    return get_file(filepath, "./static/dist/", "text/css")


@get("/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return get_file(filepath, "./static/dist/", "image/x-icon")


@get("/<filepath:re:.*\.js>")
def js(filepath):
    return get_file(filepath, "./static/dist/", "application/javascript")


@route('/')
def server_static():
    filename = "index.html"
    return get_file(filename, "./static/", "text/html")


def get_file(filename, root, contentType):
    headers = dict()
    stats = os.stat(root + filename)
    headers['Content-Length'] = str(stats.st_size)
    headers['Content-Type'] = contentType
    body = open(root + filename, "rb")
    return HTTPResponse(body, **headers)


def on_init():
    run(host='localhost', port=8008, fast=True)