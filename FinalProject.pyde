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
        self.img1 = loadImage(path+"/images/stage"+str(self.stage)+".jpg")
        self.img2 = loadImage(path+"/images/stage"+str(self.stage)+"b.jpg")
        
    def display(self):
        if self.y1>=0 or self.y1>=-1000:
            self.y1+=25
            image(self.img1, 0, self.y1, 700, 1000)
        if self.y2>=-1000:
            self.y2+=25
            image(self.img2, 0, self.y2, 700, 1000)
            #image(self.img, 0, self.y2, 700, 1000, 700, 1000, 0, 0)
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
        #self.health=100
        self.bpos=[]
        self.killed=False
        self.hit=0
        self.keyHandler={LEFT:False, RIGHT:False, UP:False}  #dictionary to set values for keyboard buttons
        self.img=loadImage(path+'/images/player.png')
        self.bullet=loadImage(path+'/images/fire.png')
        self.blast=loadImage(path+'/images/blast.png')
    
    def display(self):
        image(self.img,self.x,self.y,150,150)
            
        if self.keyHandler[LEFT]: 
            if self.x<=0:
                self.vx = 0
            else:
                self.vx = -20
        elif self.keyHandler[RIGHT]:
            if self.x >= 550:
                self.vx = 0
            else:
                self.vx = 20
        else:
            self.vx = 0    
        self.x += self.vx
        
        if self.keyHandler[UP]:
            self.bpos.append([self.x,850])
            self.keyHandler[UP]=False
        for cnt in range(len(self.bpos)):
            self.bpos[cnt][1]-=20
            image(self.bullet, self.bpos[cnt][0]+60, self.bpos[cnt][1], 30, 30)
            if t.time>=1200 and self.bpos[cnt][1]<=200 and self.bpos[cnt][1]>0 and self.bpos[cnt][0] in range(100, 570):
                self.hit+=1
                image(self.blast, self.bpos[cnt][0], 50, 150, 150)
                self.bpos[cnt][1]=-20
                if self.hit==10:
                    #t.B.state='dead'
                    self.killed=True
            elif self.bpos[cnt][1]==110 and self.bpos[cnt][0] in range(t.e.x,t.e.x+125):
                t.e.state='dead'
                self.killed=True
                self.bpos[cnt][1]=-20
                
        # for cnt in range(len(self.bpos)):
        #     if self.bpos[cnt][1]<=0:
        #         self.bpos[cnt].pop()
                
class Enemy:
    def __init__(self):
        self.x=10*randint(-5,50)
        self.img=loadImage(path+'/images/enemy.png')
        self.bullet=loadImage(path+'/images/beam.png')
        self.blast=loadImage(path+'/images/blast.png')
        self.by=150
        self.b=self.x+105
        self.state='alive'
        
    def display(self):
        if self.state=='dead':
            image(self.blast, self.x, 0, 150, 150)
            self.x=10*randint(-5,50)
            self.b=self.x+105
            self.by=150
            self.state='alive'
        
        image(self.img,self.x,0,250,150)
        image(self.bullet,self.b,self.by,30,30)
        if self.by >= 1000:
             self.by=150
        else:
            self.by+=20
        
        if self.b in range(t.s.x,t.s.x+141) and self.by in range(900,950):
            image(self.blast,t.s.x,850,150,150)
            t.health-=5
            self.by = 1000
            if t.health<=0:
                t.state='lost'

class Boss:
    def __init__(self):
        self.img=loadImage(path+'/images/boss.png')
        self.bullet=loadImage(path+'/images/beam.png')
        self.blast=loadImage(path+'/images/blast.png')
        self.state='alive'
        self.by=200
        self.bx=[200,340,480]
        self.bllt=[[choice(self.bx),self.by]]
        
    def display(self):
        image(self.img, 100, 0, 500, 200)
        #if self.state=='alive':
        for cnt in range(len(self.bllt)):
            image(self.bullet,self.bllt[cnt][0],self.bllt[cnt][1],30,30)
            self.bllt[cnt][1]+=20
            if self.bllt[cnt][0] in range(t.s.x,t.s.x+141) and self.bllt[cnt][1] in range(900, 950):
                image(self.blast, t.s.x, 850, 150, 150)
                t.health-=5
                self.bllt[cnt][1]=1000
        if t.time%20==0 and t.time!=1200:
            self.bllt.append([choice(self.bx),self.by])

class Asteroid:
    def __init__(self):
        self.x=10*randint(0,55)
        self.y=0
        self.img=loadImage(path+'/images/asteroid.png')
        self.dim= 10*randint(5,15)
        self.speed=1500/self.dim
        
    def display(self):
        image(self.img, self.x, self.y, self.dim, self.dim)
        if self.y<1000:
            self.y+=self.speed
        else:
            self.y=0
            self.x=10*randint(0,55)
            self.dim=10*randint(5,15)
            self.speed=1500/self.dim
        print(self.x)
        print(t.s.x)
        if self.x in range(t.s.x-self.dim+30,t.s.x+120) and self.y in range(875,925):
            image(t.e.blast,t.s.x,850,150,150)
            t.health-=2
            self.y=1000
            if t.health<=0:
                t.state='lost'

class Game:
    def __init__(self):
        self.stage=0
        self.x1=0
        self.x2=0
        self.y1=0
        self.y2=-1000
        self.time=1
        self.score=0
        self.health=100
        self.state = "menu"
        self.img = loadImage(path+"/images/stage0.jpg")
        self.s=SpaceShip(300,850)
        self.e=Enemy()
        self.B=Boss()
        self.a=Asteroid()
        
    def display(self):
        if self.state == 'menu':
            image(self.img, 0, 0)
            self.homescreen()
        elif self.state == 'play':
            b=Background(self.stage, self.x1, self.x2, self.y1, self.y2)
            self.x1,self.x2,self.y1,self.y2=b.display()
            self.s.display()
            #self.e.display()
            #self.B.display()
            self.a.display()
            self.scorecounter()
            self.healthpointer()
            self.time+=1
            if self.time>=1200:
                self.B.display()
            else:
                self.e.display()
            # if self.score >= 300:
            #     self.stage = 3
            # elif self.score >= 100:
            #     #self.stage = 2
            #     self.B.display()
        else:
            if self.state == 'lost':
                self.gameover()
            elif self.state=='win':
                self.gamewin()
            self.x1=0
            self.x2=0
            self.y1=0
            self.y2=-1000
            self.time=1
            self.score=0
            self.health=100
            self.img = loadImage(path+"/images/stage0.jpg")
            self.s=SpaceShip(300,850)
            self.e=Enemy()
            
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
        
    def scorecounter(self):
        if self.time%10==0:
            self.score+=1
        if self.s.killed==True:
            if self.s.hit>=10:
                if self.stage==3:
                    self.state='win'
                else:
                    self.score+=50
                    self.stage+=1
                    self.time=1
                    self.s.hit=0
            else:
                self.score+=10
            self.s.killed=False
        fill(255)
        textSize(25)
        text(self.score, 5, 30)
        
    def healthpointer(self):
        stroke(255)
        noFill()
        rect(598, 20, 101, 20)
        noStroke()
        fill(0,255,0)
        rect(599, 21, self.health, 18)
        if self.health<=0:
            self.state='lost'
        
    def gameover(self):
        textSize(100)
        fill(255,0,0)
        text("GAME OVER", 70, 500)
        fill(255)
        rect(250, 550, 220, 50, 7)
        rect(250, 650, 220, 50, 7)
        fill(0)
        textSize(32)
        text("PLAY AGAIN", 265, 585)
        text("MAIN MENU", 267, 685)
        
    def gamewin(self):
        textSize(100)
        fill(255,0,0)
        text("YOU WIN!!!", 70, 400)
        textSize(48)
        text("Score:"+str(self.score), 200, 500)
        print(self.score)
        fill(255)
        rect(250, 550, 220, 50, 7)
        rect(250, 650, 220, 50, 7)
        fill(0)
        textSize(32)
        text("PLAY AGAIN", 265, 585)
        text("MAIN MENU", 267, 685)

t=Game()
        
def setup():
    size(700, 1000)
    background(0)

def draw():
    t.display()

def mouseClicked():
    if t.state == 'menu':
        if mouseX >= 400 and mouseX <= 550 and mouseY >= 500 and mouseY <= 550:
            t.state = 'play'
            t.stage = 1
       # elif mouseX >= 370 and mouseX <= 620 and mouseY >= 600 and mouseY <= 650:
    if t.state == 'lost' or t.state=='win':
        if mouseX >= 250 and mouseX <= 470 and mouseY >= 550 and mouseY <= 600:
            t.state = 'play'
            t.stage = 1
        elif mouseX >= 250 and mouseX <= 470 and mouseY >= 650 and mouseY <= 700:
            t.state = 'menu'
            t.stage = 0
        
def keyPressed():
    if keyCode == LEFT:
        t.s.keyHandler[LEFT] = True
    elif keyCode == RIGHT:
        t.s.keyHandler[RIGHT] = True
        
def keyReleased():
    if keyCode == LEFT:
        t.s.keyHandler[LEFT] = False
    elif keyCode == RIGHT:
        t.s.keyHandler[RIGHT] = False
    elif keyCode ==UP:
        t.s.keyHandler[UP] = True        
