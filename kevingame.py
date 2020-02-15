# -*- coding: utf-8 -*-
"""Two player game. Press cursor keys or w,a,s,d
"""
def kevingame(hitpoints=100): 
 

     #p1 = windows
     #p2 = linux
    import pygame
    import random

    pygame.init()
    HITPOINTS=hitpoints
    SCREENX = 2000
    SCREENY = 2000
    FORCE_OF_GRAVITY = 9.81 # in pixel per second² .See http://en.wikipedia.org/wiki/Gravitational_acceleration 
    screen=pygame.display.set_mode((SCREENX, SCREENY)) # try out larger values and see what happens !
     
    background = pygame.image.load("backgroundweiss.jpg")
    background.convert() # no tranparency

    def newcolour():
        # any colour but black or white 
        return (random.randint(10,250), random.randint(10,250), random.randint(10,250))
     


    def write(msg="pygame is cool"):
        myfont = pygame.font.SysFont("None", 50)
        mytext = myfont.render(msg, True, (0,0,0))
        mytext = mytext.convert_alpha()
        return mytext


    class Spieler(pygame.sprite.Sprite):
        p2image = pygame.image.load("babytux.png")
        p2image = p2image.convert_alpha()
     
        p1image = pygame.image.load("1_m.png")
        p1image = p1image.convert_alpha() # take transparent color from image
        spieler = {} # a directory of all Birds, each Bird has its own number
        number = 0  

        def __init__(self):
             pygame.sprite.Sprite.__init__(self, self.groups)
             self.life = 100
             self.image =  Spieler.p1image
             self.rect = self.image.get_rect()
             self.rect.center = (500,100)
             self.hitpointsfull = HITPOINTS # maximal hitpoints
             self.hitpoints = HITPOINTS # actual hitpoints
             self.keys = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
             self.number = Spieler.number # get my personal Birdnumber
             Spieler.number+= 1           # increase the number for next Bird
             Spieler.spieler[self.number] = self # store myself into the Bird directory
             #print "my number %i Bird number %i " % (self.number, Bird.number)
             self.energie = 0
             Livebar(self)
             

        def kill(self):
                Spieler.spieler[self.number] = None # kill Bird in sprite Directory
                pygame.sprite.Sprite.kill(self) # kill the actual Bird 



        def update(self,time):
             pressed_keys = pygame.key.get_pressed()
             self.gx = 0
             self.gy = 0

             if pressed_keys[self.keys[0]]:
                      self.gy=-100
             if pressed_keys[self.keys[1]]:
                       self.gy=100
             if pressed_keys[self.keys[2]]:
                      self.gx=-100
             if pressed_keys[self.keys[3]]:
                      self.gx =100
            
             self.rect.centerx += self.gx * time
             self.rect.centery += self.gy * time
             if self.rect.centerx<0:
                 self.rect.centerx = 0         
             if self.rect.centery<0:
                 self.rect.centery = 0         
             if self.rect.centerx>SCREENX:
                 self.rect.centerx = SCREENX
             if self.rect.centery>SCREENY:
                 self.rect.centery = SCREENY
             if self.hitpoints <=0:
                 self.kill()
    class Bombe(pygame.sprite.Sprite):
        number = 0
        p2image = pygame.image.load("babytux.png")
        p2image = p2image.convert_alpha()
     
        p1image = pygame.image.load("1_m.png")
        p1image = p1image.convert_alpha() # take transparent color from image
        
        bomben1image = pygame.image.load("bombe1schaden.png")
        bomben1image = bomben1image.convert_alpha()
        bomben = {}
        
        def __init__(self, pos):
             pygame.sprite.Sprite.__init__(self, self.groups)
             self.image =   Bombe.bomben1image
             self.rect = self.image.get_rect()
             self.time=0
             self.rect.center = pos
             self.pos = pos
             self.number = Bombe.number # get my personal Birdnumber
             Bombe.number+= 1           # increase the number for next Bird
             Bombe.bomben[self.number] = self # store myself into the Bird directory

        def kill(self):
            """because i want to do some special effects (sound, directory etc.)
            before killing the Bird sprite i have to write my own kill(self)
            function and finally call pygame.sprite.Sprite.kill(self) 
            to do the 'real' killing"""
            #cry.play()
            #print Bird.birds, "..."
            for _ in range(random.randint(100,150)):
                Fragment(self.pos)
            Bombe.bomben[self.number] = None # kill Bird in sprite Directory
            pygame.sprite.Sprite.kill(self) # kill the actual Bird 
            
        def update(self,time):
             self.time += time 
             self.gx = 0
             self.gy = 0
             
             self.rect.centerx += self.gx * time
             self.rect.centery += self.gy * time
             if self.rect.centerx<0:
                 self.rect.centerx = 0         
             if self.rect.centery<0:
                 self.rect.centery = 0         
             if self.rect.centerx>SCREENX:
                 self.rect.centerx = SCREENX
             if self.rect.centery>SCREENY:
                 self.rect.centery = SCREENY
             if self.time > 2.0:
                 print "lexi bum"
                 self.kill()
            
    class Energie(pygame.sprite.Sprite):
        def __init__(self,energiewert, pos):
            
            self.energiewert= energiewert
            self.msg="blblblb"
            self.pos = pos
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.image = pygame.Surface((50,50))
            self.image.fill((255,255,255))
            self.rect=self.image.get_rect()
            #self.rect.center=((800,100))
            #self.msg="KEvin ..... rult?"
            #self.msg="Energie Spieler x: %i" %self.energiewert

        def update(self,time):
            self.image=write(self.msg)
            self.rect= self.image.get_rect()
            self.rect.center = self.pos
            if not Spieler.spieler[self.energiewert]:
                    self.kill() # kill the hitbar
            else:        
                    self.msg="Energie Spieler %i: %i" %(self.energiewert, Spieler.spieler[self.energiewert].energie) 

    class Livebar(pygame.sprite.Sprite):
            """shows a bar with the hitpoints of a Bird sprite"""
            def __init__(self, boss):
                pygame.sprite.Sprite.__init__(self,self.groups)
                self.boss = boss
                #print self.boss
                self.image = pygame.Surface((self.boss.rect.width,7))
                self.image.set_colorkey((0,0,0)) # black transparent
                pygame.draw.rect(self.image, (0,255,0), (0,0,self.boss.rect.width,7),1)
                self.rect = self.image.get_rect()
                self.oldpercent = 0
                self.bossnumber = self.boss.number # the unique number (name) of my boss
     
            def update(self, time):
                self.percent = self.boss.hitpoints / self.boss.hitpointsfull * 1.0
                #print self.percent
                if self.percent != self.oldpercent:
                    pygame.draw.rect(self.image, (0,0,0), (1,1,self.boss.rect.width-2,5)) # fill black
                    pygame.draw.rect(self.image, (0,255,0), (1,1,
                        int(self.boss.rect.width * self.percent),5),0) # fill green
                self.oldpercent = self.percent
                self.rect.centerx = self.boss.rect.centerx
                self.rect.centery = self.boss.rect.centery - self.boss.rect.height /2 - 10
                #check if boss is still alive
                if not Spieler.spieler[self.bossnumber]:
                    self.kill() # kill the hitbar

     
    class Fragment(pygame.sprite.Sprite):
        """a fragment of an exploding Bird"""
        gravity = False # fragments fall down ?
        radius= 10
        def __init__(self, pos):
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.pos = [0.0,0.0]
            self.pos[0] = pos[0]
            self.pos[1] = pos[1]
            self.image = pygame.Surface((10,10))
            self.image.set_colorkey((0,0,0)) # black transparent
            pygame.draw.circle(self.image, (random.randint(1,64),0,0), (5,5), 
                                            random.randint(2,5))
            self.image = self.image.convert_alpha()
            self.rect = self.image.get_rect()
            self.lifetime = random.random()*0.7 # max 6 seconds
            self.time = 0.0
            self.fragmentmaxspeed = 250 # try out other factors !
            self.dx = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
            self.dy = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
            
        def update(self, seconds):
            self.time += seconds
            if self.time > self.lifetime:
                self.kill() 
            self.pos[0] += self.dx * seconds
            self.pos[1] += self.dy * seconds
            if Fragment.gravity:
                self.dy += FORCE_OF_GRAVITY # gravity suck fragments down
            self.rect.centerx = round(self.pos[0],0)
            self.rect.centery = round(self.pos[1],0)
            

    class Docht(pygame.sprite.Sprite):
        images=[]
        images.append(pygame.image.load("docht4.png"))
        images.append(pygame.image.load("docht2.png"))
        images.append(pygame.image.load("docht3.png"))
        images.append(pygame.image.load("docht1.png"))
        images[0]=images[0].convert_alpha()
        images[1]=images[1].convert_alpha()
        images[2]=images[2].convert_alpha()
        images[3]=images[3].convert_alpha()
           
        def __init__(self, master):
             pygame.sprite.Sprite.__init__(self, self.groups)
             self.image =  Docht.images[0]
             
             self.rect = self.image.get_rect()
             self.time=0
             self.master=master
             self.rect.center = self.master.rect.center
             self.rect.centery -= 110
             
        def update(self,time):
            self.time+=time*10
            self.rect.centery+=int(self.time/5)
            self.image=Docht.images[int(self.time%4)]
           
            print int(self.time%4)
            if self.master.time > 2:
                self.kill()
                print "lexi bum bum"

                



    bomben = pygame.sprite.Group()
    allgroup = pygame.sprite.LayeredUpdates()
    #allsprites = (p1, p2, bomben)
    playergroup = pygame.sprite.Group()
    #allsprites = pygame.sprite.Group() 
    #spieler = pygame.sprite.Group()
    bargroup =pygame.sprite.Group()
    fragmentgroup = pygame.sprite.Group()
    #dochtgruppe=pygame.sprite.Group()
    Docht.groups = allgroup 
    Spieler.groups=allgroup, playergroup
    Fragment.groups=  allgroup , fragmentgroup
    Energie.groups= allgroup 
    #Docht.groups=allsprites, dochtgruppe
    Livebar.groups =  bargroup, allgroup
    Bombe.groups=  allgroup 
    Bombe._layer = 2
    Fragment._layer = 5
    Docht._layer = 1
    Spieler._layer = 3
    Livebar._layer = 4

    p1= Spieler()
    p2= Spieler()
    p2.image=Spieler.p2image 
    p2.rect.center= (100,100) 
    p2.keys=[pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d] 
    pressed_keys = pygame.key.get_pressed()
    p2.energie=0







    #allsprites = pygame.sprite.LayeredUpdates(spieler, bomben)
    screen.blit(background, (0,0))     #draw background on screen (overwriting all)

    clock = pygame.time.Clock()
    mainloop = True
    FPS = 30 # desired framerate in frames per second.
    e1 =Energie(0,(180,25))
    e2 =Energie(1, (570,25))
    playtime=0.0
    energietime=0.0
    while mainloop:
        # do all this each framehttp://www.spielend-programmieren.at/pythongamebook/doku.php
        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        seconds = milliseconds / 1000.0 # seconds passed since last frame
        #clock.tick(FPS) # do not go faster than this framerate
        playtime+=seconds
        energietime+=seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False # pygame window closed by user
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False # user pressed ESC
                if event.key == pygame.K_e and p2.energie >= 10:
                    #bomben.add(Bombe(p2.rect.center))
                    Docht(Bombe(p2.rect.center))
                    p2.energie-=10.0
                if event.key == pygame.K_DELETE and p1.energie >= 10:
                    #bomben.add(Bombe(p1.rect.center))
                    Docht(Bombe(p1.rect.center))
                    p1.energie-=10.0 
                if event.key == pygame.K_h:
                    Fragment((50,50))
        pressed_keys = pygame.key.get_pressed()
        if energietime > 1.0:
            energietime=0.0
            p1.energie+=1.0
            p2.energie+=1.0
        pygame.display.set_caption("pygame is running with %.2f frames per second" % clock.get_fps())
        # only blit the part of the background where the marvin was (cleanrect)
        #cleanrect2 = background.subsurface((p2x, p2y, p2.get_width(), p2.get_height()))
        #screen.blit(cleanrect2, (p2x, p2y))
        #cleanrect = background.subsurface((p1x, p1y, p1.get_width(), p1.get_height()))
        #screen.blit(cleanrect, (p1x, p1y)) # comment out this line for a funny effect !
        #calculate new center of marvin
        # time based movement. No matter how busy the cpu and how low the framerate,
        # movement speed will always be constant.
         
        
        #b2x += 5
        #bx += 5
        #if bombe2x - p1x < 25 and bombe2y - p1y < 25:
        #    p1x = 0
        #    p1y = 0
        
        #if bombex - p2x < 25 and bombey - p2y < 25:
        #    p2x = 0
        #    p2y = 0    
            
       
        for player in playergroup:
            crashgroup = pygame.sprite.spritecollide(player, fragmentgroup, False, pygame.sprite.collide_circle)
            for fraggi in crashgroup:
                player.hitpoints -=0.5
                #print player.hitpoints
                
        allgroup.clear(screen, background)
        #allsprites = pygame.sprite.LayeredUpdates(spieler, bomben) 
        allgroup.update(seconds)
        allgroup.draw(screen)
        
        #dochtgruppe.clear(screen, background)
        #bomben.clear(screen, background)
       # spieler.clear(screen, background)
        #dochtgruppe.update(seconds)
        #spieler.update(seconds)
        #bomben.update(seconds)
        #dochtgruppe.draw(screen)
       # bomben.draw(screen)
        #spieler.draw(screen)
        if not Spieler.spieler[0]:
            mainloop=False
            winner="spieler2"
        elif not Spieler.spieler[1]:
            mainloop=False
            winner="spieler1"    
        pygame.display.flip()          # flip the screen 30 times a second
    # Game Over   
    return winner

if __name__=="__main__":
    kevingame()
