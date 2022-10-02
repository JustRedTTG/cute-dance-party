from datetime import datetime
import time
import random

import hexicapi.server as server
import pickle, os, _thread
class Group:
    def __init__(self,num,name='...'):
        self.id = ''
        self.num = num
        self.pos = (325, 250)
        self.health = 3
        self.direction = 1  # right
        self.moving = False
        self.active = True
        self.name = name

server.ip = "127.0.0.1"
server.port = 81

bank = '1234567'
colors = [(255,0,0),(255,0,255),(0,255,0),(255, 165, 0),(255,255,51),(50,50,255),(100,100,255)]

def arbi_reverse(bin):
    return pickle.loads(bin)
def arbi(*args):
    return pickle.dumps(args)
p1,p2,p3 = Group(1),Group(2),Group(3)
p1.pos = (300,225)
p2.pos = (325,250)
p3.pos = (350,275)
p1.active = False
p2.active = False
p3.active = False
disco = []
state = 0
actiontime = []
chosen = 0

def action():
    global actiontime,state
    now = datetime.now()
    actiontime = [now.minute, now.second]
def check():
    global actiontime
    now = datetime.now()
    return ( ( now.minute - actiontime[0] ) * 60 ) + ( now.second - actiontime[1] )
action()
def make():
    cx,cy=0,0
    list = []
    while cy < 18:
        while cx < 18:
            c = random.randint(0, len(colors) - 1)
            list.append(c)
            cx+=1
        cx = 0
        cy+=1
    return list

@server.client.app
def info(Client,message):
    if message == 'bank':
        server.client.send(Client,bank)
    if message == 'colors':
        server.client.send(Client,arbi(*colors))


@server.client.app
def game(Client,message):
    global p1,p2,p3,state,disco,chosen

    if message == 'lobby':
        server.client.send(Client,arbi(p1.active,p2.active,p3.active))
    elif message == 'join':
        if p1.active:
            if p2.active:
                if p3.active:
                    server.client.send(Client,'full')
                else:
                    server.client.send(Client,'3')
                    p3.id = Client['id']
                    p3.name = Client['username']
                    p3.active = True
            else:
                server.client.send(Client,'2')
                p2.id = Client['id']
                p2.name = Client['username']
                p2.active = True
        else:
            server.client.send(Client,'1')
            p1.id = Client['id']
            p1.name = Client['username']
            p1.active = True
    elif type(message) == bytes and b'getpos ' in message:
        pos = message.replace(b'getpos ',b'')
        pl = arbi_reverse(pos)[0]
        if Client['id'] == p1.id:
            p1 = pl
        elif Client['id'] == p2.id:
            p2 = pl
        elif Client['id'] == p3.id:
            p3 = pl
        #print(p1.direction,datetime.now().strftime("%H:%M:%S"))
        server.client.send(Client,arbi(p1,p2,p3))
    elif message == 'bye' or message == 'leave':
        print(message,Client['id'])
        if Client['id'] == p1.id:
            p1.active = False
        elif Client['id'] == p2.id:
            p2.active = False
        elif Client['id'] == p3.id:
            p3.active = False
    elif message == 'info':
        if p1.active: #and p2.active and p3.active:
            if state == 0:
                state = 1
                action()
            elif state == 1 and check() > 3:
                state = 1.5
                action()
                disco = make()
                chosen = random.randint(0, len(colors) - 1)
            elif state == 1.5 and check() > 1:
                state = 2
                action()
            elif state == 2 and check() > 10:
                state = 3
                action()
            elif state == 3 and check() > 1:
                state = 1
                action()
        else:
            state = 0
        if state == 1.5:
            server.client.send(Client,arbi(state,disco))
        elif state == 2:
            server.client.send(Client,arbi(state,check()/2,20,chosen))
        else:
            server.client.send(Client,arbi(state))


@server.client.app_disconnect
def game(connection):
    v = connection['id']
    if v == p1.id:
        p1.active = False
    elif v == p2.id:
        p2.active = False
    elif v == p3.id:
        p3.active = False
    return False
server.allowGuest['info'] = True
server.allowGuest['game'] = True

#_thread.start_new_thread(handler,())
server.run()
