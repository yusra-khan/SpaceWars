add_library("minim") 
import os 
from random import * 
path = os.getcwd() #sets current directory
player = Minim(this)
homemusic = player.loadFile(path + '/music/music.mp3')
stage1 = player.loadFile(path + '/music/Stage1.mp3')
stage2 = player.loadFile(path + '/music/Stage2.mp3')
stage3 = player.loadFile(path + '/music/Stage3.mp3')
slaser = player.loadFile(path + '/music/slaser.mp3')
elaser = player.loadFile(path + '/music/elaser.mp3')
gamewin = player.loadFile(path + '/music/gamewin.mp3')
gamelose = player.loadFile(path + '/music/gamelose.mp3')
blast = player.loadFile(path + '/music/blast.mp3')
highscore=0

class Background:
    def __init__(self, x1, x2, y1, y2):
        global stage
        self.x1=x1 #x-coordinate of 1st background image
        self.x2=x2 #x-coordinate of 2nd background image
        self.y1=y1 #y-coordinate of 1st background image
        self.y2=y2 #y-coordinate of 2nd background image
        self.img1 = loadImage(path+"/images/stage"+str(stage)+".jpg") #background image
        self.img2 = loadImage(path+"/images/stage"+str(stage)+"b.jpg") #inverted background image
        
    def display(self):
        if self.y1>=0 or self.y1>=-1000: 
            self.y1+=25
            image(self.img1, 0, self.y1, 700, 1000) #Shows movement of background
        if self.y2>=-1000:
            self.y2+=25
            image(self.img2, 0, self.y2, 700, 1000) #Shows movement of 2nd image background
        if self.y1==0:
            self.y2=-1000 #Brings back image back to its original position allowing a continuous moving background
        if self.y2==0:
            self.y1=-1000
            
        return self.x1,self.x2,self.y1,self.y2

class SpaceShip:
    def __init__(self,x,y):
        self.x=x #x-coordinate of spaceship
        self.y=y #y-coordinate of spaceship
        self.vx=0 #to set the speed of the spaceship
        self.bpos=[] #list to keep track of bullet position
        self.killed=False #if the enemy is killed
        self.hit=0 #number of times the enemy is hit by a bullet
        self.hit2=0 #number of times the 2nd enemy in stage 3 is hit
        self.keyHandler={LEFT:False, RIGHT:False, UP:False}  #dictionary to set values for keyboard buttons
        self.img=loadImage(path+'/images/player.png')
        self.bullet=loadImage(path+'/images/fire.png')
        self.blast=loadImage(path+'/images/blast.png')
    
    def display(self):
        image(self.img,self.x,self.y,150,150) #displays image of spaceship
            
        if self.keyHandler[LEFT]:  
            if self.x<=0:
                self.vx = 0
            else:
                self.vx = -30  #Allows movement towards left when the 'LEFT' key is pressed
        elif self.keyHandler[RIGHT]:
            if self.x >= 550:
                self.vx = 0
            else:
                self.vx = 30  #Allows movement towards right when the 'RIGHT' key is pressed
        else:
            self.vx = 0    
        self.x += self.vx  # x coordinate changes depending on the key pressed allowing movement
        
        if self.keyHandler[UP]: 
            self.bpos.append([self.x,850]) #shooting of a bullet when 'UP' key is pressed
            slaser.rewind()
            slaser.play()  # Plays bullet sound 
            self.keyHandler[UP]=False #Allows another bullet to be fired
        for cnt in range(len(self.bpos)): 
            self.bpos[cnt][1]-=20 #spaceship bullet speed allowing movement
            image(self.bullet, self.bpos[cnt][0]+60, self.bpos[cnt][1], 30, 30) #shows image of bullet 
            if t.time>=1200 and self.bpos[cnt][1]<=150 and self.bpos[cnt][1]>0 and self.bpos[cnt][0] in range(t.B.x-40, t.B.x+210): #sets condition and range to hit Boss ship
                self.hit+=1 #keeps count of hits
                image(self.blast, self.bpos[cnt][0], 50, 150, 150) #shows blast image when bullet collides with enemy
                blast.rewind()
                blast.play() #plays sound of blast when bullet collides with boss ship
                self.bpos[cnt][1]=-20
                if self.hit==40: #boss dies when hit 40 times
                    self.killed=True
            else:
                if self.bpos[cnt][1]==110 and self.bpos[cnt][0] in range(t.e.x,t.e.x+125): #sets condition and range to hit enemy ship
                    self.hit+=1 #keeps cound of hits
                    image(self.blast, t.e.x, 0, 150, 150) #shows image of blast
                    blast.rewind()
                    blast.play() #plays sound of blast when bullet collides with enemy
                    if self.hit==2: #enemy ship dies after 2 hits
                        t.e.state='dead'
                        self.killed=True
                        self.bpos[cnt][1]=-20
                if stage==3 and self.bpos[cnt][1]==110 and self.bpos[cnt][0] in range(t.e.x2,t.e.x2+125):
                    self.hit2+=1 #keeps track of hits of 2nd enemy ship in stage 3
                    image(self.blast, t.e.x2, 0, 150, 150)
                    blast.rewind()
                    blast.play()
                    if self.hit2==2: #2nd enemy spaceship also dies after 2 hits
                        t.e.state2='dead'
                        self.killed=True
                        self.bpos[cnt][1]=-20
                
class Enemy:
    def __init__(self):
        global stage
        self.x=10*randint(0,50) #x-coordinate of enemy
        self.x2=10*randint(0,50) #x-coordinate of 2nd enemy in stage 3
        self.y=10 #speed of enemy
        self.y2=10 #speed of 2nd enemy in stage 3
        self.choose=randint(1,3) #to choose a random enemy from the 3 options
        self.img=loadImage(path+'/images/enemy'+str(self.choose)+'.png')
        self.bullet=loadImage(path+'/images/beam.png')
        self.blast=loadImage(path+'/images/blast.png')
        self.by=150 #y-coordinate of enemy bullet
        self.b=self.x+105 #x-coordinate of enemy bullet
        self.b2=self.x2+105 #x-coordinate of enemy bullet from the 2nd enemy
        self.state='alive' #state of enemy
        self.state2='alive' #state of 2nd enemy
        self.epos=[] #list of enemy bullets' positions
        self.epos2=[] #list of 2nd enemy's bullet positions
        
    def display(self):
        if self.state=='dead': #resets vriables for respawning
            self.x=10*randint(0,50) #selects random x-coordinate to spawn enemy spaceship
            self.y=10
            self.b=self.x+105
            self.state='alive'
            self.choose=randint(1,3)
            self.img=loadImage(path+'/images/enemy'+str(self.choose)+'.png') #randomly selects one of enemy ship from among 3 choices
                    
        if self.state2=='dead':
            self.x2=10*randint(0,50) #randomly selects x-coordinate of enemy spaceship when previous one dies
            self.y2=10
            self.b2=self.x2+105
            self.state2='alive'

        image(self.img,self.x,0,250,150)
        if stage == 3: #spawns 2 enemy ships in stage 3
            image(self.img, self.x2, 0, 250, 150) 
            
        if t.time<200 and stage == 1:   #rate of firing bullet starts slowly for enemy space ship in stage 1 and increases after specific time interval
            if t.time%40==0: 
                self.epos.append([self.b,self.by]) #appends bullet position to a list to allow movement of bullets independent of the movement of ship
                elaser.rewind() 
                elaser.play() #plays sound of enemy bullet
        elif t.time<600 and t.time>=200 and stage == 1:
            if t.time%30==0: #rate of firing bullet for enemy spaceship increased from previous
                self.epos.append([self.b,self.by])
                elaser.rewind()
                elaser.play()
        else:
            if t.time%20==0:#rate of firing bullet for enemy spaceship increased from previous
                self.epos.append([self.b,self.by])
                elaser.rewind()
                elaser.play()

        for cnt in range(len(self.epos)):
            image(self.bullet, self.epos[cnt][0],self.epos[cnt][1],30,30) #displays image of enemy bullet
            self.epos[cnt][1]+=20 #sets speed of vertical movement of bullet
            if self.epos[cnt][0] in range(t.s.x,t.s.x+141) and self.epos[cnt][1] in range(900,950): #to check if bullet hits spaceship
                if t.p.flag==True:
                    t.health+=10 # if spaceship is hit when having absorber powerup, health increases by 10
                    self.epos[cnt][1] = 1000 #bullet goes off the screen
                else:
                    image(self.blast,t.s.x,850,150,150) #displays image of blast when hit by enemy bullets
                    blast.rewind()
                    blast.play() #plays blast sound effect
                    t.health-=20 #health decreases by 20 when hit by enemy bullet
                    self.epos[cnt][1] = 1000
                    if t.health<=0: #lose condition if health becomes less than or equal to 0
                        t.state='lost'   
            
        if stage==3: 
            if t.time%20==0:
                self.epos2.append([self.b2,self.by]) #appends bullet for 2nd enemy ship in stage 3
            for cnt in range(len(self.epos2)):
                image(self.bullet, self.epos2[cnt][0],self.epos2[cnt][1],30,30) #displays bullet
                self.epos2[cnt][1]+=20 #allows vertical movement of enemy bullet
                if self.epos2[cnt][0] in range(t.s.x,t.s.x+141) and self.epos2[cnt][1] in range(900,950):
                    if t.p.flag==True:
                        t.health+=10 # if bullet hits absorber powerup, health increases by 10
                        self.epos2[cnt][1] = 1000
                    else:
                        image(self.blast,t.s.x,850,150,150) #displays image of blast when hit by enemy bullets
                        blast.rewind()
                        blast.play() #plays blast sound effect
                        t.health-=20 #if bullet hits spaceship, health decreases by 20
                        self.epos2[cnt][1] = 1000
                        if t.health<=0: #lose condition if health becomes less than or equal to 0
                            t.state='lost'                   
        if stage==2 or stage==3: #for movement of enemy spaceship in stage 2 and 3
            self.x+=self.y #movement along x-axis
            self.b=self.x+105
            if self.x<10 or self.x>550: #prevents from going out of the frame
                self.y=-1*self.y #reverses motion of enemy spaceship when reaches end of frame
        if stage==3: #for movement of the 2nd enemy spaceship in stage 3
            self.x2-=self.y2
            self.b2=self.x2+105
            if self.x2<10 or self.x2>550:
                self.y2=-1*self.y2
           
class Boss:
    def __init__(self):
        global stage
        self.img1=loadImage(path+"/images/boss1.png")
        self.img2=loadImage(path+"/images/boss2.png")
        self.img3=loadImage(path+"/images/boss3.png")
        self.bullet=loadImage(path+'/images/beam.png')
        self.blast=loadImage(path+'/images/blast.png')
        self.state='alive'
        self.by=[] #list for the y-coordinates of every set of 5 boss bullets
        self.x=200 #x-coordinate of boss
        self.y=10 #speed of boss
        self.bx=[self.x+25,self.x+75,self.x+150,self.x+225,self.x+275] #x-coordinates of the 5 boss bullets
        self.bllt=[] #list of the x-coordinates of every set of x-coordinates
        
    def display(self):
        if stage==1: #determining which boss to display according to the stage
            image(self.img1, self.x, 0, 300, 200)
        elif stage==2:
            image(self.img2, self.x, 0, 300, 200)
        elif stage==3:
            image(self.img3, self.x, 0, 300, 200)
        
        if t.time%20==0: #creating a new set of bullets after every interval of 20 frames
            self.bllt.append(self.bx)
            self.by.append([200,200,200,200,200])
            elaser.rewind()
            elaser.play() #sound of enemy bullets
        for c in range(len(self.bllt)): #to display all the bullets as they travel down the screen 
            if stage==3: #to create the spreading effect of bullets in stage 3
                self.bllt[c][0]-=8
                self.bllt[c][1]-=4
                self.bllt[c][3]+=4
                self.bllt[c][4]+=8
            for cnt in range(len(self.bx)): #to display each of the 5 bullets in a set
                self.by[c][cnt]+=20 #speed of the bullets
                image(self.bullet,self.bllt[c][cnt],self.by[c][cnt],30,30)
                if self.bllt[c][cnt] in range(t.s.x,t.s.x+141) and self.by[c][cnt] in range(900, 950): #if a bullet hits the spaceship
                    if t.p.flag==True: #health increases if absorber is present
                        t.health+=10
                        self.by[c][cnt] = 1000
                    else:
                        image(self.blast,t.s.x,850,150,150)
                        blast.rewind()
                        blast.play()
                        t.health-=20
                        self.by[c][cnt] = 1000
                        if t.health<=0:
                            t.state='lost'   
        if stage == 2 or stage==3: #movement of boss in stages 2 and 3
            self.x+=self.y
            if self.x<10 or self.x>400:
                self.y=-1*self.y 
            self.bx=[self.x+25,self.x+75,self.x+150,self.x+225,self.x+275]             
            
               

class Asteroid:
    def __init__(self):
        global stage
        self.x=10*randint(0,55) #random x-coordinate of asteroid
        self.x2=10*randint(0,55) #random x-coordinate of 2nd asteroid
        self.y=0 #y-coordinate of asteroid
        self.y2=0 #y-coordinate of 2nd asteroid
        self.img=loadImage(path+'/images/asteroid.png')
        self.dim= 10*randint(5,15) #random size of asteroid
        self.dim2=10*randint(5,15)#random size of 2nd asteroid
        self.speed=1500/self.dim #speed of asteroid
        self.speed2=1500/self.dim2 #speed of 2nd asteroid
        
    def display(self):
        image(self.img, self.x, self.y, self.dim, self.dim) #1st asteroid
        if stage==2 or stage==3:
            image(self.img, self.x2, self.y2, self.dim2, self.dim2) #2nd asteroid
        if self.y<1000: #movement down the screen
            self.y+=self.speed
        else:
            self.y=0 #resetting variables when asteroid goes out of frame
            self.x=10*randint(0,55)
            self.dim=10*randint(5,15)
            self.speed=1500/self.dim
        if stage==2 or stage==3: #movement of 2nd asteroid
            if self.y2<1000:
                self.y2+=self.speed2
            else:
                self.y2=0
                self.x2=10*randint(0,55)
                self.dim2=10*randint(5,15)
                self.speed2=1500/self.dim2
        if self.x in range(t.s.x-self.dim+30,t.s.x+120) and self.y in range(875,925): #if asteroid hits spaceship
            image(t.e.blast,t.s.x,850,150,150)
            blast.rewind()
            blast.play()
            t.health-=10
            self.y=1000
            if t.health<=0:
                t.state='lost'
        if stage!=1 and self.x2 in range(t.s.x-self.dim2+30,t.s.x+120) and self.y2 in range(875,925): #if the 2nd asteroid hits spaceship
            image(t.e.blast,t.s.x,850,150,150)
            blast.rewind()
            blast.play()
            t.health-=10
            self.y2=1000
            if t.health<=0:
                t.state='lost'
                
class Powerups:
    def __init__(self):
        self.x = 10 * randint(0,60) #random x-coordinate of powerup
        self.y = 0 #y-coordinate of powerup
        self.aspirin = loadImage(path + '/images/health.png') #health booster
        self.absorb = loadImage(path + '/images/absorber.png') #absorber
        self.healthlist= [] #list of position of health booster
        self.absorblist= [] #list of position of absorber
        self.time=1 #how long will the absorber be in effect
        self.flag=False #if spaceship catches the absorber
        
    def health(self):
        if t.time%1000==0: #appearance of health booster after every 1000 frames
            self.x = 10 * randint(0,60)
            self.healthlist.append([self.x,self.y])
        
        for i in range(len(self.healthlist)):
            image(self.aspirin,self.healthlist[i][0],self.healthlist[i][1],100,100) #display health booster
            self.healthlist[i][1]+=10
            if self.healthlist[i][0] in range(t.s.x-70,t.s.x+120) and self.healthlist[i][1] in range(875,950): #restore health if spaceship catches the booster
                if t.health<100:
                    t.health=100
                self.healthlist[i][1]=1000
            
    def absorber(self):
        if t.time%450==0: #appearance of absorber after every 450 frames
            self.x = 10 * randint(0,60)
            self.absorblist.append([self.x,self.y])
        for j in range(len(self.absorblist)):
            image(self.absorb,self.absorblist[j][0],self.absorblist[j][1],100,100) #display absorber
            self.absorblist[j][1]+=15
            if self.absorblist[j][0] in range(t.s.x-70,t.s.x+120) and self.absorblist[j][1] in range(875,925): #bring absorber in effect if spaceship catches it
                self.flag=True
                self.absorblist[j][1]=1000
            if self.flag==True:
                if self.time<=50: #keep absorber for 50 frames
                    image(self.absorb,t.s.x-25,t.s.y,200,200)
                    self.time+=1
                else:
                    self.flag=False
                    self.time=1

    
class Game:
    def __init__(self):
        global stage, highscore
        self.x1=0 #x-coordinate of 1st image of background
        self.x2=0 #x-coordinate of 2nd image of background
        self.y1=0 #y-coordinate of 1st image of background
        self.y2=-1000 #y-coordinate of 2nd image of background
        self.time=1 #keep track of frames
        self.score=0
        self.health=100
        self.state = "menu"
        self.img = loadImage(path+"/images/stage0.jpg")
        self.s=SpaceShip(300,850)
        self.e=Enemy()
        self.B=Boss()
        self.a=Asteroid()
        self.p=Powerups()
        
    def display(self):
        if self.state == 'menu': #display homescreen
            image(self.img, 0, 0)
            self.homescreen()
        elif self.state == 'play':
            b=Background(self.x1, self.x2, self.y1, self.y2)
            self.x1,self.x2,self.y1,self.y2=b.display()
            self.s.display()
            self.a.display()
            self.scorecounter()
            self.p.health()
            self.p.absorber()
            self.time+=1
            if self.time>=900 and (stage ==1 or stage == 2): #bring boss after 900 frames for stage 1 and 2
                self.B.display()
            elif self.time>=1200 and stage == 3: #bring boss after 1200 frames for stage 3
                self.B.display()
            else:
                self.e.display()
            self.healthpointer()
            homemusic.pause()
            if stage == 1: #play different music for every stage
                stage3.pause()
                stage1.play()
            elif stage == 2:
                stage1.pause()
                stage2.play()
            elif stage == 3:
                stage1.pause()
                stage2.pause()
                stage3.play()
        elif self.state=='transition': #transition between stages
            background(0)
            textSize(100)
            fill(0,0,255)
            text("STAGE "+str(stage), 150, 500)
            self.s.bpos=[] #refresh all the lists
            self.e.epos=[]
            self.e.epos2=[]
            self.B.bllt=[]
            self.B.by=[]
            self.p.healthlist=[]
            self.p.absorblist=[]
            self.time+=1
            if self.time==100: #display transition screen for 100 frames
                self.state='play'
                self.time=1
        else:
            if self.state == 'lost': #call gameover screen
                self.gameover()
                gamelose.play()
            elif self.state=='win': #call gamewin screen
                self.gamewin()
                gamewin.play()
           
            
    def homescreen(self):
        fill(255)
        stroke(255)
        rect(400, 500, 150, 50, 7) #make play and instructions buttons
        rect(370, 600, 250, 50, 7)
        font = loadFont("OCRAExtended-48.vlw")
        fill(0)
        textSize(32)
        text("PLAY", 435, 535)
        text("INSTRUCTIONS", 380, 635)
        fill(255)
        textFont(font)
        textSize(120)
        text("SPACE", 10, 150) #display title
        text("WARS", 10, 250)
        stage1.pause()
        stage2.pause()
        stage3.pause()
        homemusic.play() #background music
        
    def scorecounter(self):
        global stage
        if self.time%10==0: #increase score by 1 every 10 frames
            self.score+=1
        if self.s.killed==True: #when an enemy is killed
            if self.s.hit>=40: #when a boss is killed
                if stage==3: #game is won if stage 3 boss is killed
                    self.score+=50
                    self.state='win'
                else:
                    self.score+=50 #score increases by 50 when a boss is killed
                    stage+=1 #next stage
                    self.time=1
                    self.state='transition'
            else:
                self.score+=10 #score increases by 10 when a normal enemy is killed
            if self.s.hit2==2: #resetting the number of hits on the enemy
                self.s.hit2=0
            else:
                self.s.hit=0
            self.s.killed=False
        fill(255)
        textSize(25)
        text(self.score, 5, 30) #display the score in the corner
        
    def healthpointer(self):
        if self.health<0: #to avoid health running out from the back if it goes into negatives
            self.health=0
        stroke(255)
        noFill()
        rect(598, 20, 101, 20)#display the health bar
        noStroke()
        fill(0,255,0)
        rect(599, 21, self.health, 18)
        if self.health<=0: #game is lost when health becomes 0
            self.state='lost'
        
    def gameover(self):
        textSize(100)
        fill(255,0,0)
        text("GAME OVER", 70, 400) #display the game over message
        textSize(48)
        text("Score:"+str(self.score), 250, 500) #display final score        
        fill(255)
        rect(250, 550, 220, 50, 7) #create play again and menu buttons
        rect(250, 650, 220, 50, 7)
        fill(0)
        textSize(32)
        text("PLAY AGAIN", 265, 585)
        text("MAIN MENU", 267, 685)
        homemusic.rewind() #resets all background musics
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
        text("YOU WIN!!!", 70, 400) #display game win message
        textSize(48)
        text("Score: "+str(self.score), 250, 500) #display final score
        fill(255)
        rect(250, 550, 220, 50, 7) #create play again and menu buttons
        rect(250, 650, 220, 50, 7)
        fill(0)
        textSize(32)
        text("PLAY AGAIN", 265, 585)
        text("MAIN MENU", 267, 685)
        homemusic.rewind() #resets all background musics
        homemusic.pause()
        stage1.rewind()
        stage1.pause()
        stage2.rewind()
        stage2.pause()
        stage3.rewind()
        stage3.pause()

stage=0 #initialize stage
t=Game()
        
def setup():
    size(700, 1000) #initialize screen
    background(0)

def draw():
    global stage, highscore
    t.display()

def mouseClicked():
    global stage, highscore
    if t.state == 'menu': #define function of play and instructions buttons on the homescreen
        if mouseX >= 400 and mouseX <= 550 and mouseY >= 500 and mouseY <= 550:
            t.state = 'play'
            stage = 1
       # elif mouseX >= 370 and mouseX <= 620 and mouseY >= 600 and mouseY <= 650:
    if t.state == 'lost' or t.state=='win': #reset all variables when game ends
        t.x1=0
        t.x2=0
        t.y1=0
        t.y2=-1000
        t.time=1
        t.health=100
        t.img = loadImage(path+"/images/stage0.jpg")
        t.s=SpaceShip(300,850)
        t.e=Enemy()
        t.p=Powerups()
        t.a=Asteroid()
        t.B=Boss()
        if t.state == 'lost': #play game lose sound
            gamelose.rewind()
            gamelose.pause()
        elif t.state == 'win': #play game win sound
            gamewin.rewind()
            gamewin.pause()
        if mouseX >= 250 and mouseX <= 470 and mouseY >= 550 and mouseY <= 600: ##define function of play button
            t.state = 'play'
            stage = 1
            t.score=0
        elif mouseX >= 250 and mouseX <= 470 and mouseY >= 650 and mouseY <= 700: #define function of menu button
            t.state = 'menu'
            stage = 0
            t.score=0


                
def keyPressed(): #for movement of spaceship
    if keyCode == LEFT:
        t.s.keyHandler[LEFT] = True
    elif keyCode == RIGHT:
        t.s.keyHandler[RIGHT] = True
        
def keyReleased():
    if keyCode == LEFT:
        t.s.keyHandler[LEFT] = False
    elif keyCode == RIGHT:
        t.s.keyHandler[RIGHT] = False
    elif keyCode ==UP: #for shooting bullets
        t.s.keyHandler[UP] = True        
