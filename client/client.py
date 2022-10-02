import os, pickle
import random

from datetime import datetime
try:
    import pgerom as pe
except:
    os.system("pip install pgerom")
    os.system("pip3 install pgerom")
    import pgerom as pe

name=''
while name == '':
    if os.path.exists('data'):# and False:
        name = pe.load('data')[0]
    else:
        name=input("Enter name > ")
        if name != '':
            pe.save('data',name)
            print('please start again!')
            exit()
#
try:
    import hexicapi.client as client
except:
    os.system("pip install hexicapi")
    os.system("pip3 install hexicapi")
    import hexicapi.client as client
import _thread
pe.init()

# PYGAME / PYGAMEEXTRA INITIALIZATION

clock = pe.pygame.time.Clock()
font = pe.pygame.font.SysFont("Arial", 18)
pe.display.make((650,500),"Cute Dance Party")

client.ip = '127.0.0.1'
client.port = 81
@client.on_calf
def authentication_fail():
    print("authentication error")
    exit()
@client.on_calf
def connection_fail():
    print('connection error')
    exit()
@client.on_calf
def disconnect():
    print('closing due to disconnect...')
    exit()

def arbi(bin):
    return pickle.loads(bin)
def arbi_reverse(*args):
    return pickle.dumps(args)
pe.fill.full(pe.color.white,update=True)
loading_img = pe.image('files/loading.png',(650,500),(0,0))
loading_img.display()
pe.display.update()

Client = client.run('info','_','_')
Client.id = Client.heartbeat()
bank = ''
colors = []
Client.send('bank')
bank = Client.receive()
Client.send('colors')
colors = arbi(Client.receive())
class Group:
    def __init__(self):
        pass
images = Group()
animation_speed = 0.5
total_load = '6'
heartbeat = 0

print("Loading game data, please wait...")
# Load game data
print("Loading 1/"+total_load)
images.p_t = pe.image('files/p_tilt.png',(55,109),(170,40))
images.a_t = pe.image('files/a_tilt.png',(55,109),(225,40))
images.r_t = pe.image('files/r_tilt.png',(51,109),(280,40))
images.t_t = pe.image('files/t_tilt.png',(44,109),(327,40))
images.y_t = pe.image('files/y_tilt.png',(46,109),(371,40))
images.qem = pe.Sprite(pe.sheet('files/!.png',(74,74)),(74,74),(417,40))
images.qem.step = 0.2
images.qem1 = pe.Sprite(pe.sheet('files/!.png',(74,74)),(74,74),(433,40))
images.qem1.frame = 2
images.qem1.step = 0.2
images.qem2 = pe.Sprite(pe.sheet('files/!.png',(74,74)),(74,74),(449,40))
images.qem1.frame = 3
images.qem2.step = 0.2
images.front = pe.image('files/front.png',(400,400),(125,50))
# death animations
print("Loading 2/"+total_load)
images.death1 = pe.Sprite(pe.sheet('files/dead.png',(601,502)),(65,62),(50,50))
images.death2 = pe.Sprite(pe.sheet('files/dead.png',(601,502)),(65,62),(50,50))
images.death3 = pe.Sprite(pe.sheet('files/dead.png',(601,502)),(65,62),(50,50))
images.death1.step = animation_speed
# idle animations
print("Loading 3/"+total_load)
images.idle1r = pe.Sprite(pe.sheet('files/idle_right.png',(454,454)),(40,40),(50,100))
images.idle2r = pe.Sprite(pe.sheet('files/idle_right.png',(454,454)),(40,40),(50,50))
images.idle3r = pe.Sprite(pe.sheet('files/idle_right.png',(454,454)),(40,40),(325-20,250-20))
images.idler_load = pe.Sprite(pe.sheet('files/idle_right.png',(454,454)),(100,100),(325-50,250-50))
images.idle1r.step = animation_speed
images.idle2r.step = animation_speed
images.idle3r.step = animation_speed
images.idler_load.step = animation_speed
print("Loading 4/"+total_load)
images.idle1l = pe.Sprite(pe.sheet('files/idle_left.png',(454,454)),(40,40),(50,150))
images.idle2l = pe.Sprite(pe.sheet('files/idle_left.png',(454,454)),(40,40),(50,50))
images.idle3l = pe.Sprite(pe.sheet('files/idle_left.png',(454,454)),(40,40),(50,50))
images.idle1l.step = animation_speed
images.idle2l.step = animation_speed
images.idle3l.step = animation_speed
print("Loading 5/"+total_load)
images.run1r = pe.Sprite(pe.sheet('files/run_right.png',(454,454)),(40,40),(50,100))
images.run2r = pe.Sprite(pe.sheet('files/run_right.png',(454,454)),(40,40),(50,50))
images.run3r = pe.Sprite(pe.sheet('files/run_right.png',(454,454)),(40,40),(325-20,250-20))
images.run1r.step = animation_speed
images.run2r.step = animation_speed
images.run3r.step = animation_speed
print("Loading 6/"+total_load)
images.run1l = pe.Sprite(pe.sheet('files/run_left.png',(454,454)),(40,40),(50,100))
images.run2l = pe.Sprite(pe.sheet('files/run_left.png',(454,454)),(40,40),(50,50))
images.run3l = pe.Sprite(pe.sheet('files/run_left.png',(454,454)),(40,40),(325-20,250-20))
images.run1l.step = animation_speed
images.run2l.step = animation_speed
images.run3l.step = animation_speed
font = pe.pygame.font.SysFont('Comic Sans MS', 10)
print("Loading complete!")

animate_logo = False
pro = 0
pro_g = 5
pro_a = True
speed = 10
allowmove = False

class Player():
    def __init__(self, num, nameV = '...'):
        self.id = Client.id
        self.num = num
        self.pos = (325,250)
        self.health = 3
        self.direction = 1 # right
        self.moving = False
        self.active = True
        self.name = nameV
        if num == 1:
            self.death = images.death1
            self.idle_right = images.idle1r
            self.idle_left = images.idle1l
            self.run_right = images.run1r
            self.run_left = images.run1l
        elif num == 2:
            self.death = images.death2
            self.idle_right = images.idle2r
            self.idle_left = images.idle2l
            self.run_right = images.run2r
            self.run_left = images.run2l
        elif num == 3:
            self.death = images.death3
            self.idle_right = images.idle3r
            self.idle_left = images.idle3l
            self.run_right = images.run3r
            self.run_left = images.run3l
    def animate(self):
        if self.health <= 0:
            pos = list(self.pos)
            pos[0] += 960
            self.death.position = pos
            if self.death.frame > self.death.frames - 2:
                self.death.step = 0.0001
            self.death.init_position()
            self.death.display()
            if self.death.step == 0.0001:
                self.death.frame = self.death.frames - 1
            elif self.death.step < 0.0001:
                self.death.step = 0.0001
        elif self.moving:
            pos = list(self.pos)
            pos[0] += 380
            if self.direction == 0:
                self.run_left.position = pos
                self.run_left.init_position()
                self.run_left.display()
            elif self.direction == 1:
                self.run_right.position = pos
                self.run_right.init_position()
                self.run_right.display()
        else:
            pos = list(self.pos)
            pos[0] += 300
            if self.direction == 0:
                self.idle_left.position = pos
                self.idle_left.init_position()
                self.idle_left.display()
            elif self.direction == 1:
                self.idle_right.position = pos
                self.idle_right.init_position()
                self.idle_right.display()
        text = font.render(self.name, False, pe.color.black)
        pos = (self.pos[0] - 10 - text.get_width()/2,self.pos[1] - 40)
        pe.draw.rect(pe.color.white,(pos[0],pos[1],text.get_width(),text.get_height()),0)
        pe.display.blit.rect(text,pos)
        #pe.draw.rect(pe.color.blue,(me.pos[0] - 10, me.pos[1] - 10, 20, 30),1)
        #pe.draw.rect(pe.color.blue,(me.pos[0] - 6, me.pos[1] + 15, 17, 7),1)
def logo():
    global pro,pro_a
    if pro < pro_g and pro_a and animate_logo:
        pro+=1
    elif pro > pro_g*-1 and not pro_a and animate_logo:
        pro-=1
    elif animate_logo:
        pro_a = not pro_a
    else:
        pro = 0
        pro_a = True
    if animate_logo:
        x = list(images.p_t.position) # P
        x[1]+=pro
        images.p_t.position = tuple(x)

        x = list(images.a_t.position) # A
        x[1]-=pro
        images.a_t.position = tuple(x)

        x = list(images.r_t.position) # R
        x[1]+=pro
        images.r_t.position = tuple(x)

        x = list(images.t_t.position) # T
        x[1]-=pro
        images.t_t.position = tuple(x)

        x = list(images.y_t.position) # Y
        x[1]+=pro
        images.y_t.position = tuple(x)
    images.p_t.display(layer=1)
    images.a_t.display(layer=1)
    images.r_t.display(layer=1)
    images.t_t.display(layer=1)
    images.y_t.display(layer=1)
    if not animate_logo:
        images.idler_load.display()
    if animate_logo:
        x = list(images.p_t.position)  # P
        x[1] -= pro
        images.p_t.position = tuple(x)

        x = list(images.a_t.position)  # A
        x[1] += pro
        images.a_t.position = tuple(x)

        x = list(images.r_t.position)  # R
        x[1] -= pro
        images.r_t.position = tuple(x)

        x = list(images.t_t.position)  # T
        x[1] += pro
        images.t_t.position = tuple(x)

        x = list(images.y_t.position)  # Y
        x[1] -= pro
        images.y_t.position = tuple(x)
    if animate_logo:
        images.qem.step = 0.2
        images.qem1.step = 0.2
        images.qem2.step = 0.2
    else:
        images.qem.step = 0
        images.qem1.step = 0
        images.qem2.step = 0
    images.qem.display()
    images.qem1.display()
    images.qem2.display()
setting = False
new_ps = (325,250)
last_p = (0,0)
def events():
    global new_ps,last_p
    for pe.event.c in pe.event.get():
        if pe.event.quitcheck():
            Client.send('leave')
            Client.disconnect()
    if not menu > 0:
        return
    m_r = pe.pygame.Rect(pe.mouse.pos()[0]-1,pe.mouse.pos()[1]-1,1,1)
    p_r = pe.pygame.Rect(me.pos[0] - 10, me.pos[1] - 10, 20, 30)
    brd = pe.pygame.Rect(125+p_r.w+20, 70, 400-(p_r.w*2)-40, 400-p_r.h-40)
    pe.draw.rect(pe.color.blue,brd,5)
    if allowmove and me.health > 0 and not p_r.colliderect(m_r) :
        new = pe.math.lerp(me.pos,pe.mouse.pos(),min( pe.math.dist(me.pos,pe.mouse.pos()) / speed, speed ))
        new = (int(new[0]),int(new[1]))
        p_r = pe.pygame.Rect(new[0] - 10, new[1] - 10, 20, 30)
        if p_r.colliderect(brd):
            new_ps = new
        else:
            new_ps = me.pos
        mpl = me.pos
        if pe.math.dist((mpl[0],0),(new_ps[0],0)) > -1 and True:
            if pe.math.dist((pe.mouse.pos()[0],0),(me.pos[0] - 10, 0)) < pe.math.dist((pe.mouse.pos()[0],0),(me.pos[0] + 10, 0)):
                me.direction = 0
            elif pe.math.dist((pe.mouse.pos()[0],0),(me.pos[0] - 10, 0)) > pe.math.dist((pe.mouse.pos()[0],0),(me.pos[0] + 10, 0)):
                me.direction = 1
            else:
                me.direction = 2
        me.moving = True
        pe.pygame.mouse.set_visible(1)
    elif allowmove:
        pe.pygame.mouse.set_visible(0)
        me.moving = False
        last_p = me.pos

menu = 0
p1 = None
p2 = None
p3 = None
me = None
disco = []
state = 0
time = 0
maxtime = 20
chosen = 0
touch = False
dama = False
def mover(f:Player,t:Player):
    t.id = f.id
    t.num = f.num
    t.pos = f.pos
    t.health = f.health
    t.direction = f.direction
    t.moving = f.moving
    t.active = f.active
    t.name = f.name
    return t
def get_pos():
    global heartbeat,p1,p2,p3,state,disco,time,maxtime,chosen,touch,dama
    while True:
        #print('pre',me.direction, datetime.now().strftime("%H:%M:%S"))
        me.pos = new_ps
        mer = mover(me,Group())
        #print(mer.direction, datetime.now().strftime("%H:%M:%S"))
        Client.send(b'getpos '+arbi_reverse(mer))
        sp = Client.receive()
        if sp != False:
            p1r, p2r, p3r = arbi(sp)
            if p1 != me:
                p1 = mover(p1r,p1)
            if p2 != me:
                p2 = mover(p2r,p2)
            if p3 != me:
                p3 = mover(p3r,p3)
        else:
            Client.disconnect()
        Client.send('info')
        result = arbi(Client.receive())
        state = result[0]
        if state == 1.5:
            disco = result[1]
        elif state == 0:
            disco = []
        elif state == 2:
            dama = False
            time = result[1]
            maxtime = result[2]
            chosen = result[3]
        elif state == 3 and not dama:
            if not touch:
                me.health -= 1
            dama = True
        #pe.time.sleep(10)

def get_game_info():
    global Client, menu, p1, p2, p3, animate_logo,Player,me,allowmove
    def join():
        global animate_logo,menu,allowmove
        allowmove = True
        Client.send('join')
        res = Client.receive()
        if res == 'full':
            animate_logo = True
            print("Game has already started, try again later")
        elif int(res) == me.num:
            _thread.start_new_thread(get_pos, ())
            animate_logo = True
            menu += 1
    Client = client.run('game', name, '_')
    Client.id = Client.heartbeat()
    Client.send('lobby')
    p1a,p2a,p3a = arbi(Client.receive())
    p1 = Player(1)
    p2 = Player(2)
    p3 = Player(3)
    p1.active = False
    p2.active = False
    p3.active = False
    if p1a:
        p1 = Player(1)
    else:
        p1 = Player(1,name)
        me = p1
        join()
        return
    if p2a:
        p2 = Player(2)
    else:
        p2 = Player(2,name)
        me = p2
        join()
        return
    if p3a:
        animate_logo = True
        print("Game has already started, try again later")
    else:
        p3 = Player(3,name)
        me = p3
        join()
        return

_thread.start_new_thread(get_game_info,())

pe.Layer[0][1] = (0,-500)
def draw_b():
    global touch
    x, y = 145, 70
    cx, cy = 0, 0
    s = 20
    c = colors[0]
    i=0
    touch = False
    pr = pe.pygame.Rect(me.pos[0] - 6, me.pos[1] + 15, 17, 7)
    while cy < 18:
        while cx < 18:
            try:
                c = colors[disco[i]]
                pe.draw.rect(c,(x+(cx*s),y+(cy*s),s,s),0)
                rectB = pe.pygame.Rect(x+(cx*s),y+(cy*s),s,s)
                if disco[i] == chosen:
                    #pe.draw.rect(pe.color.white,rectB,5)
                    if rectB.colliderect(pr):
                        touch = True
            except:
                pass
            cx+=1
            i+=1
        cx = 0
        cy+=1
    #pe.draw.rect(pe.color.white, pr, 4)
while True:
    pe.fill.full(pe.color.black)
    heartbeat+=1
    if menu == 0:
        events()
        logo()
    elif menu == 1:
        events()
        logo()
        if pe.Layer[0][1][1]<0:
            pe.Layer[0][1] = list(pe.Layer[0][1])
            pe.Layer[0][1][1] += 20
            pe.Layer[0][1] = tuple(pe.Layer[0][1])
        else:
            animate_logo = False
        pe.draw.rect(pe.color.darkgray, (125, 50, 400, 400), 0)
        draw_b()
        images.front.display()
        if state == 2 and time != maxtime:
            # bar
            pe.draw.line(pe.color.white,(325-202,25),(325+202,25),10)
            pe.draw.line(pe.color.black,(325-201,25),(325+201,25),8)
            pe.draw.line(pe.color.yellow,(325-200,25),(325-200+( (20-time)*20 ),25),6)
            # cube
            pe.draw.rect(pe.color.white,(550,25,75,75),0)
            if touch:
                pe.draw.rect(pe.color.green,(551,26,73,73),0)
            else:
                pe.draw.rect(pe.color.red,(553,28,69,69),0)
            pe.draw.rect(pe.color.black,(555,30,65,65),0)
            pe.draw.rect(colors[chosen],(560,35,55,55),0)
        xP,yP = 550, 110
        s = (75-3*4)/4
        for h in range(me.health+1):
            pe.draw.rect(pe.color.red,(xP,yP,s - 3,s - 3),5)
            xP += s + 6
        if me.moving:
            posV = me.pos
            mp = pe.mouse.pos()
            last = posV
            boolV = False
            d = 10#pe.math.dist(posV,pe.mouse.pos()) / 10
            while pe.math.dist(posV,pe.mouse.pos()) > speed:
                last = posV
                posV = pe.math.lerp(posV,mp,d)
                if boolV:
                    pe.draw.line(pe.color.white,pe.math.lerp(last,posV,d+2),pe.math.lerp(posV,last,d+2),7)
                    pe.draw.line(pe.color.black,pe.math.lerp(last,posV,d+1),pe.math.lerp(posV,last,d+1),5)
                    pe.draw.line(pe.color.red,last,posV,3)
                    boolV = False
                else:
                    boolV = True
        if p1 != me and p1.active:
            p1.animate()
        if p2 != me and p2.active:
            p2.animate()
        if p3 != me and p3.active:
            p3.animate()
        me.animate()
    clock.tick(60)
    pe.display.update()
    #print(clock.get_fps())# print FPS
