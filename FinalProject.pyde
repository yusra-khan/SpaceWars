add_library("minim")
import os 
from random import *
path = os.getcwd()
player = Minim(this)

class Background:
    def __init__(self, stage, x1, x2, y1, y2):
        self.stage=stage
        self.x1=x1
        self.x2=x2
        self.y1=y1
        self.y2=y2
        self.img = loadImage(path+"/images/stage"+str(self.stage)+".jpg")
        
    def display(self):
        if self.y1>=0 or self.y1>=-1000:
            self.y1+=25
            image(self.img, 0, self.y1, 700, 1000)
        if self.y2>=-1000:
            self.y2+=25
            image(self.img, 0, self.y2, 700, 1000, 700, 1000, 0, 0)
        if self.y1==0:
            self.y2=-1000
        if self.y2==0:
            self.y1=-1000
            
        return self.x1,self.x2,self.y1,self.y2

class SpaceShip:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.d=y
        self.vx=0
        self.vy=0
        self.keyHandler={LEFT:False, RIGHT:False, UP:False}  #dictionary to set values for keyboard buttons
        self.img=loadImage(path+'/images/player.png')
        self.bpos=[]
    
    def movement(self):
        image(self.img,self.x,self.y,150,150)
            
        if self.keyHandler[LEFT]: 
            if self.x<=0:
                self.vx = 0
            else:
                self.vx = -10
        elif self.keyHandler[RIGHT]:
            if self.x >= 550:
                self.vx = 0
            else:
                self.vx = 10
        else:
            self.vx = 0    
        self.x += self.vx
        
class Bullet:
    def __init__(self):
        #global xy
        #self.x = x
        self.y=850
        #self.vy=0
        self.fire=loadImage(path+'/images/fire.png')
        #self.keyHandler={LEFT:False, RIGHT:False, UP:False}  #dictionary to set values for keyboard buttons
        
    
    def display(self):
        for cnt in range(len(s.bpos)):
            s.bpos[cnt][1]-=10
            image(self.fire, s.bpos[cnt][0]+60, s.bpos[cnt][1], 30,30)
        # if self.y <=0:
        #     s.keyHandler[UP] = False
        
class Enemy:
    def __init__(self):
        #global Health
        #self.y=randint(-10,10)
        self.x=10*randint(0,55)
        self.img=loadImage(path+'/images/enemy.png')
        self.bullet=loadImage(path+'/images/beam.png')
        self.blast=loadImage(path+'/images/blast.png')
        self.by=150
        self.b=self.x+105
        
    def display(self):
        #global Game
        # self.x+=self.y
        # if self.x<=10 or self.x>=850:
        #     self.y=-1*self.y            
        
        image(self.img,self.x,0,250,150)
        image(self.bullet,self.b,self.by,30,30)
        if self.by == 1000:
             self.by=150
        else:
            self.by+=10
        
        if self.b in range(s.x,s.x+141) and self.by in range(900,950):
            #print(g.x)
            #print('Blast')
            image(self.blast,s.x,850,150,150)
            
 
        
class Game:
    def __init__(self):
        self.stage=0
        self.x1=0
        self.x2=0
        self.y1=0
        self.y2=-1000
        #self.state = "menu"
        self.img = loadImage(path+"/images/stage0.jpg")
        global s, e
        s=SpaceShip(300,850)
        e=Enemy()
        
    def display(self):
        if self.stage == 0:
            image(self.img, 0, 0)
            self.homescreen()
        else:
            b=Background(self.stage, self.x1, self.x2, self.y1, self.y2)
            self.x1,self.x2,self.y1,self.y2=b.display()
            s.movement()
            e.display()
            if s.keyHandler[UP]:
                B.display()
        
            
    def homescreen(self):
        fill(255)
        stroke(255)
        rect(400, 500, 150, 50, 7)
        rect(370, 600, 250, 50, 7)
        font = loadFont("OCRAExtended-48.vlw")
        fill(0)
        textSize(32)
        text("PLAY", 435, 535)
        text("INSTRUCTIONS", 380, 635)
        fill(255)
        textFont(font)
        textSize(120)
        text("SPACE", 10, 150)
        text("WARS", 10, 250)
        

t=Game()
        
def setup():
    size(700, 1000)
    background(0)

def draw():
    t.display()

def mouseClicked():
    if t.stage == 0:
        if mouseX >= 400 and mouseX <= 550 and mouseY >= 500 and mouseY <= 550:
            t.stage = 1
       #     t.state = "play"
       # elif mouseX >= 370 and mouseX <= 620 and mouseY >= 600 and mouseY <= 650:

def keyPressed():
    if keyCode == LEFT:
        s.keyHandler[LEFT] = True
    elif keyCode == RIGHT:
        s.keyHandler[RIGHT] = True
    elif keyCode == UP:
        s.bpos.append([s.x, 850])
        global B
        B=Bullet()
        s.keyHandler[UP] = True

        
def keyReleased():
    if keyCode == LEFT:
        s.keyHandler[LEFT] = False
    elif keyCode == RIGHT:
        s.keyHandler[RIGHT] = False            
