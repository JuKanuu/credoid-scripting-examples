from bottle import run, post, get, response, route, static_file, delete, HTTPResponse
import json
import time
import socket
import os


class Door(object):

    def __init__(self, doorID, doorStatus):
        self.doorID = doorID
        self.doorStatus = doorStatus  # False  == closed

    def __nonzero__(self):
        return self.doorStatus % 2 == 0


class DoorContiner(object):
    def __init__(self):
        self.doorList = []

    def add_to_list(self, doorObject):
        self.doorList.append(doorObject)
        return

    def change_door_status(self, doorID, action):
        if action == 'open':
            self.doorList[int(doorID)].doorStatus = True
            # context.turn_output_on(str(doorID))
        elif action == 'close':
            self.doorList[int(doorID)].doorStatus = False
            # context.turn_output_off(str(doorID))
        return


class Group(object):
    def __init__(self, groupID, groupStatus):
        self.groupID = groupID
        self.groupStatus = groupStatus  # false = closed
        self.doorIdList = []

    def __nonzero__(self):
        return self.groupStatus % 2 == 0


class GroupContainer(object):
    def __init__(self):
        self.groupList = []

    def group_list(self):
        return self.groupList

    def add_door_to_group(self, groupID, doorID):
        for group in self.groupList:
            if group.groupID == int(groupID):
                if doorID not in group.doorIdList:
                    group.doorIdList.append(int(doorID))
                    return
        return

    def return_group_doors(self, groupID):
        for group in self.groupList:
            if group.groupID == int(groupID):
                return group.doorIdList
        return

    def add_group_to_list(self, group):
        for i in range(len(self.groupList)):
            if (group.groupID == self.groupList[i].groupID):
                print "Already in the list"
                return

        self.groupList.append(group)
        return

    def remove_from_group(self, groupID, doorID):
        for group in self.groupList:
            if group.groupID == int(groupID):
                group.doorIdList.remove(int(doorID))
            else:
                "door not in group"
        return

    def control_group_doors(self, groupID, action):

        if action == 'open':
            for group in self.groupList:
                if int(groupID) != group.groupID and group.groupStatus == True:
                    response.status = 400
                    print "Other group open"
                    return response.status

            for group in self.groupList:
                if group.groupID == int(groupID):
                    group.groupStatus = True
                    for door in group.doorIdList:
                        change_door_status(door, 'open')


        elif action == 'close':
            for group in self.groupList:
                if group.groupID == int(groupID):
                    group.groupStatus = False
                    for door in group.doorIdList:
                        doorContainer.change_door_status(door, 'close')


doorContainer = DoorContiner()
groupContainer = GroupContainer()


# create doors
@post('/door/<count>')
def door(count):
    response.headers['Content-Type'] = 'text/html'
    response.headers['Cache-Control'] = 'no-cache'
    for i in range(int(count)):
        newDoor = Door(i, False)
        doorContainer.add_to_list(newDoor)
    return


door(8)


# create group
@post('/create/<groupID>')
def create_group(groupID):
    response.headers['Content-Type'] = 'text/html'
    response.headers['Cache-Control'] = 'no-cache'
    newGroup = Group(groupID, False)
    groupContainer.add_group_to_list(newGroup)
    return


create_group(1)
create_group(2)


# assign door to group
@post('/assign/<groupID>/<doorID>')
def door_assign(groupID, doorID):
    response.set_header('Access-Control-Allow-Origin', '*')
    response.add_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS, DELETE')
    response.headers['Content-Type'] = 'text/html'
    response.headers['Cache-Control'] = 'no-cache'
    groupContainer.add_door_to_group(groupID, doorID)
    return


# delete from group
@post('/remove/<groupID>/<doorID>')
def delete_door_from_group(groupID, doorID):
    response.set_header('Access-Control-Allow-Origin', '*')
    response.add_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS, DELETE')
    response.headers['Content-Type'] = 'text/html'
    response.headers['Cache-Control'] = 'no-cache'
    groupContainer.remove_from_group(groupID, doorID)
    return


# change door status
@post('/change/<doorID>/<action>')
def change_door_status(doorID, action):
    response.set_header('Access-Control-Allow-Origin', '*')
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Content-Length'] = ''
    doorContainer.change_door_status(doorID, action)
    return


# retrusn all doors
@get('/doorlist')
def alldoors():
    response.set_header('Access-Control-Allow-Origin', '*')
    response.add_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS, DELETE')
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    output = [p.__dict__ for p in doorContainer.doorList]
    return json.dumps(output)


# return group list
@get('/grouplist')
def allgroups():
    response.set_header('Access-Control-Allow-Origin', '*')
    response.add_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS, DELETE')
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    output = [p.__dict__ for p in groupContainer.groupList]
    return json.dumps(output)


# return group door list
@get('/groupdoorlist/<groupID>')
def group_door_list(groupID):
    response.set_header('Access-Control-Allow-Origin', '*')
    response.add_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS, DELETE')
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps(groupContainer.return_group_doors(groupID))


# Open and close Group doors
@post('/controlgroup/<groupID>/<action>')
def control_group(groupID, action):
    response.set_header('Access-Control-Allow-Origin', '*')
    response.add_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS, DELETE')
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return groupContainer.control_group_doors(groupID, action)


@get("/css/<filepath:re:.*\.css>")
def css(filepath):
    return get_file(filepath, "./css/", "text/css")


@get("/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return get_file(filepath, "./static/dist/", "image/x-icon")


@get("/dist/<filepath:re:.*\.js>")
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



run(host='localhost', port=8000, fast=True)