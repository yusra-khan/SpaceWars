add_library("minim")
import os 
from random import *
path = os.getcwd()
player = Minim(this)
homemusic = player.loadFile(path + '/music/music.mp3')
stage1 = player.loadFile(path + '/music/Stage1.mp3')
stage2 = player.loadFile(path + '/music/Stage2.mp3')
stage3 = player.loadFile(path + '/music/Stage3.mp3')
slaser = player.loadFile(path + '/music/slaser.mp3')

class Background:
    def __init__(self, x1, x2, y1, y2):
        #self.stage=stage
        global stage
        self.x1=x1
        self.x2=x2
        self.y1=y1
        self.y2=y2
        self.img1 = loadImage(path+"/images/stage"+str(stage)+".jpg")
        self.img2 = loadImage(path+"/images/stage"+str(stage)+"b.jpg")
        
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
        #global stage
        self.x=x
        self.y=y
        self.d=y
        self.vx=0
        self.vy=0
        #self.health=100
        self.bpos=[]
        self.killed=False
        self.hit=0
        self.hit2=0
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
                self.vx = -30
        elif self.keyHandler[RIGHT]:
            if self.x >= 550:
                self.vx = 0
            else:
                self.vx = 30
        else:
            self.vx = 0    
        self.x += self.vx
        
        if self.keyHandler[UP]:
            self.bpos.append([self.x,850])
            slaser.rewind()
            slaser.play()
            self.keyHandler[UP]=False
        for cnt in range(len(self.bpos)):
            self.bpos[cnt][1]-=20
            image(self.bullet, self.bpos[cnt][0]+60, self.bpos[cnt][1], 30, 30)
            if t.time>=1200 and self.bpos[cnt][1]<=150 and self.bpos[cnt][1]>0 and self.bpos[cnt][0] in range(t.B.x, t.B.x+230):
                self.hit+=1
                image(self.blast, self.bpos[cnt][0], 50, 150, 150)
                self.bpos[cnt][1]=-20
                if self.hit==40:
                    #t.B.state='dead'
                    self.killed=True
            else:
                if self.bpos[cnt][1]==110 and self.bpos[cnt][0] in range(t.e.x,t.e.x+125):
                    self.hit+=1
                    image(self.blast, t.e.x, 0, 150, 150)
                    if self.hit==2:
                        t.e.state='dead'
                        self.killed=True
                        self.bpos[cnt][1]=-20
                if stage==3 and self.bpos[cnt][1]==110 and self.bpos[cnt][0] in range(t.e.x2,t.e.x2+125):
                    self.hit2+=1
                    image(self.blast, t.e.x2, 0, 150, 150)
                    if self.hit2==2:
                        t.e.state2='dead'
                        self.killed=True
                        self.bpos[cnt][1]=-20
                
        # for cnt in range(len(self.bpos)):
        #     if self.bpos[cnt][1]<=0:
        #         self.bpos[cnt].pop()
                
class Enemy:
    def __init__(self):
        global stage
        self.x=10*randint(0,50)
        self.x2=10*randint(0,50)
        self.y=10
        self.y2=10
        self.img=loadImage(path+'/images/enemy.png')
        self.bullet=loadImage(path+'/images/beam.png')
        self.blast=loadImage(path+'/images/blast.png')
        self.by=150
        self.b=self.x+105
        self.b2=self.x2+105
        self.state='alive'
        self.state2='alive'
        self.epos=[]
        self.epos2=[]
        
    def display(self):
        if self.state=='dead':
            #image(self.blast, self.x, 0, 150, 150)
            self.x=10*randint(0,50)
            self.y=10
            self.b=self.x+105
            self.state='alive'
                    
        if self.state2=='dead':
            #image(self.blast, self.x, 0, 150, 150)
            self.x2=10*randint(0,50)
            self.y2=10
            self.b2=self.x2+105
            self.state2='alive'

        image(self.img,self.x,0,250,150)
        if stage == 3:
            image(self.img, self.x2, 0, 250, 150)
            
        if t.time%20==0:
            self.epos.append([self.b,self.by])
            #print(self.epos)
        for cnt in range(len(self.epos)):
                # if self.epos[cnt][1]>=1000:
                #     self.epos[cnt][1]=150
                # else:
            image(self.bullet, self.epos[cnt][0],self.epos[cnt][1],30,30)
            self.epos[cnt][1]+=20
            if self.epos[cnt][0] in range(t.s.x,t.s.x+141) and self.epos[cnt][1] in range(900,950):
                image(self.blast,t.s.x,850,150,150)
                t.health-=20
                self.epos[cnt][1] = 1000
                if t.health<=0:
                    t.state='lost'   
            
        if stage==3:
            if t.time%20==0:
                self.epos2.append([self.b2,self.by])
            for cnt in range(len(self.epos2)):
                    # if self.epos[cnt][1]>=1000:
                    #     self.epos[cnt][1]=150
                    # else:
                image(self.bullet, self.epos2[cnt][0],self.epos2[cnt][1],30,30)
                self.epos2[cnt][1]+=20
                if self.epos2[cnt][0] in range(t.s.x,t.s.x+141) and self.epos2[cnt][1] in range(900,950):
                    image(self.blast,t.s.x,850,150,150)
                    t.health-=20
                    self.epos2[cnt][1] = 1000
                    if t.health<=0:
                        t.state='lost'   
                
        if stage==2:
            self.x+=self.y
            self.b=self.x+105
            if self.x<10 or self.x>550:
                self.y=-1*self.y 
        if stage==3:
            self.x+=self.y
            self.b=self.x+105
            if self.x<10 or self.x>550:
                self.y=-1*self.y 
            self.x2-=self.y2
            self.b2=self.x2+105
            if self.x2<10 or self.x2>550:
                self.y2=-1*self.y2
           
class Boss:
    def __init__(self):
        #self.stage=stage
        global stage
        self.img1=loadImage(path+"/images/boss1.png")
        self.img2=loadImage(path+"/images/boss2.png")
        self.img3=loadImage(path+"/images/boss3.png")
        self.bullet=loadImage(path+'/images/beam.png')
        self.blast=loadImage(path+'/images/blast.png')
        self.state='alive'
        self.by=200
        self.x=200
        self.y=10
        self.bx=[self.x+25,self.x+75,self.x+150,self.x+225,self.x+275]
        self.bllt=[]
        self.time=0
        
    def display(self):
        if stage==1:
            image(self.img1, self.x, 0, 300, 200)
        elif stage==2:
            image(self.img2, self.x, 0, 300, 200)
        elif stage==3:
            image(self.img3, self.x, 0, 300, 200)
        # if self.time<=50:
        #     rect(400, 500, 150, 50, 7)
        #     font = loadFont("OCRAExtended-48.vlw")
        #     fill(0)
        #     textSize(32)
        #     text("HA HA", 435, 535)

        self.time+=1
        if t.time%20==0:
            self.bllt.append([self.bx,self.by])
        for c in range(len(self.bllt)):
            self.bllt[c][1]+=20
            for cnt in range(len(self.bx)):
                image(self.bullet,self.bllt[c][0][cnt],self.bllt[c][1],30,30)
                if self.bllt[c][0][cnt] in range(t.s.x,t.s.x+141) and self.bllt[c][1] in range(900, 950):
                    image(self.blast, t.s.x, 850, 150, 150)
                    t.health-=20
                    self.bllt[c][1]=1000

        if stage == 2 or stage==3:
            self.x+=self.y
            #self.b=self.x+105
            if self.x<10 or self.x>400:
                self.y=-1*self.y 
            self.bx=[self.x+25,self.x+75,self.x+150,self.x+225,self.x+275]    

class Asteroid:
    def __init__(self):
        global stage
        self.x=10*randint(0,55)
        self.x2=10*randint(0,55)
        self.y=0
        self.y2=0
        self.img=loadImage(path+'/images/asteroid.png')
        self.dim= 10*randint(5,15)
        self.dim2=10*randint(5,15)
        self.speed=1500/self.dim
        self.speed2=1500/self.dim2
        
    def display(self):
        image(self.img, self.x, self.y, self.dim, self.dim)
        if stage==2 or stage==3:
            while self.x2 in range(self.x,self.x+self.dim):
                self.x2=10*randint(0,55)
            image(self.img, self.x2, self.y2, self.dim2, self.dim2)
        if self.y<1000:
            self.y+=self.speed
        else:
            self.y=0
            self.x=10*randint(0,55)
            self.dim=10*randint(5,15)
            self.speed=1500/self.dim
        if stage==2 or stage==3:
            if self.y2<1000:
                self.y2+=self.speed2
            else:
                self.y2=0
                self.x2=10*randint(0,55)
                self.dim2=10*randint(5,15)
                self.speed2=1500/self.dim2
        if self.x in range(t.s.x-self.dim+30,t.s.x+120) and self.y in range(875,925):
            image(t.e.blast,t.s.x,850,150,150)
            t.health-=10
            self.y=1000
            if t.health<=0:
                t.state='lost'
        if stage!=1 and self.x2 in range(t.s.x-self.dim2+30,t.s.x+120) and self.y2 in range(875,925):
            image(t.e.blast,t.s.x,850,150,150)
            t.health-=10
            self.y2=1000
            if t.health<=0:
                t.state='lost'

class Game:
    def __init__(self):
        global stage
        #stage=0
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
            b=Background(self.x1, self.x2, self.y1, self.y2)
            self.x1,self.x2,self.y1,self.y2=b.display()
            self.s.display()
            #self.e.display()
            #self.B.display()
            self.a.display()
            self.scorecounter()
            self.healthpointer()
            self.time+=1
            if self.time>=1200:
                #B=Boss(self.stage)
                self.B.display()
            else:
                self.e.display()
            # if self.score >= 300:
            #     self.stage = 3
            # elif self.score >= 100:
            #     #self.stage = 2
            #     self.B.display()
            homemusic.pause()
            if stage == 1:
                stage3.pause()
                stage1.play()
            elif stage == 2:
                stage1.pause()
                stage2.play()
            elif stage == 3:
                stage1.pause()
                stage2.pause()
                stage3.play()
        else:
            if self.state == 'lost':
                self.gameover()
            elif self.state=='win':
                self.gamewin()
           
            
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
        stage1.pause()
        stage2.pause()
        stage3.pause()
        homemusic.play()
        
    def scorecounter(self):
        global stage
        if self.time%10==0:
            self.score+=1
        if self.s.killed==True:
            if self.s.hit>=40:
                if stage==3:
                    self.state='win'
                else:
                    self.score+=50
                    stage+=1
                    self.B.time=0
                    self.time=1
                    #self.s.hit=0
            else:
                self.score+=10
            if self.s.hit2==2:
                self.s.hit2=0
            else:
                self.s.hit=0
            self.s.killed=False
        fill(255)
        textSize(25)
        text(self.score, 5, 30)
        
    def healthpointer(self):
        if self.health<0:
            self.health=0
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
        homemusic.rewind()
        homemusic.pause()
        stage1.rewind()
        stage1.pause()
        stage2.rewind()
        stage2.pause()
        stage3.rewind()
        stage3.pause()
        
        
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
        stage1.rewind()
        stage1.pause()
        stage2.rewind()
        stage2.pause()
        stage3.rewind()
        stage3.pause()

#global stage
stage=0
t=Game()
        
def setup():
    size(700, 1000)
    background(0)

def draw():
    global stage
    t.display()

def mouseClicked():
    global stage
    if t.state == 'menu':
        if mouseX >= 400 and mouseX <= 550 and mouseY >= 500 and mouseY <= 550:
            t.state = 'play'
            stage = 3
       # elif mouseX >= 370 and mouseX <= 620 and mouseY >= 600 and mouseY <= 650:
    if t.state == 'lost' or t.state=='win':
        t.x1=0
        t.x2=0
        t.y1=0
        t.y2=-1000
        t.time=1
        t.health=100
        t.score=0
        t.img = loadImage(path+"/images/stage0.jpg")
        t.s=SpaceShip(300,850)
        t.e=Enemy()
        if mouseX >= 250 and mouseX <= 470 and mouseY >= 550 and mouseY <= 600:
            t.state = 'play'
            stage = 1
        elif mouseX >= 250 and mouseX <= 470 and mouseY >= 650 and mouseY <= 700:
            t.state = 'menu'
            stage = 0
            
        
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
