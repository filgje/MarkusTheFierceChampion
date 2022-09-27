
import pygame #importerer pygame og random modulen
import random

play = True #Hovedvariabel - styrer om spillet skal kjøres

#insert her
while play: #hovedloop
    pygame.init() #initierer pygame og alle modulene inni
    clock = pygame.time.Clock() #Lager en intern klokke i pygame

    s_height = 500 #Vinduhøyde
    s_width = 1000 #Vindubredde
    
    win = pygame.display.set_mode((s_width, s_height)) #definerer vinduet med bredden og høyden
    pygame.display.set_caption("Markus, The Fierce warrior") #gir spillet et navn

    room = 1  # Styrer rommet man er i

    songs = ['Musikk.mid', 'BossMusikk.mid'] #Sanger

    retning = [0, 1, 2, 3, 4] # definerer retningen mannen peker mot
    
    #Bildene for retnignene og bevegelsene for spiller, kistene, knivene, fiendene
    walkRight = [pygame.image.load("R12.png"), pygame.image.load("R22.png"), pygame.image.load("R32.png"),
                 pygame.image.load("R42.png")]
    walkDown = [pygame.image.load("F12.png"), pygame.image.load("F22.png"), pygame.image.load("F32.png"),
                pygame.image.load("F42.png")]
    walkLeft = [pygame.image.load("L12.png"), pygame.image.load("L22.png"), pygame.image.load("L32.png"),
                pygame.image.load("L42.png")]
    walkUp = [pygame.image.load("B12.png"), pygame.image.load("B22.png"), pygame.image.load("B32.png"),
              pygame.image.load("B42.png")]
    kister = [pygame.image.load("Kiste.png"), pygame.image.load("KisteÅpen.png")]
    kniver = [pygame.image.load("KnivH.png"), pygame.image.load("KnivV.png"), pygame.image.load("KnivN.png"),
              pygame.image.load("KnivO.png")]
    hjerter = [pygame.image.load("Hjerte.png"), pygame.image.load("HjerteTom.png")]
    firespirit = [pygame.image.load("Fire1.png"), pygame.image.load("Fire2.png"), pygame.image.load("Fire3.png")]
    icespirit = [pygame.image.load("IceElement1.png"), pygame.image.load("IceElement2.png"),
                 pygame.image.load("IceElement3.png")]
    
    #Spawnkoordinatene til enemies
    spawnx = [50, 900, 100, 850]
    spawny = [50, 400, 100, 350]

    fireballs = [] #Tomme lister for angrepene til spiller
    specials = []
    projectiles = []
    special_delay = 0


    class player(object): #Klasse for spiller
        def __init__(self, x, y, width, height, health): #Definerer variabler for spilleren
            self.x = x
            self.y = y
            self.height = height #Dimensjoner
            self.width = width
            self.vel = 8 #Hastighet
            self.health = health #Liv
            self.hitbox = (self.x, self.y, self.width, self.height)
            self.middle_x = self.x + (self.width / 2)
            self.middle_y = self.y + (self.height / 2)
            self.walkCount = False #Sjekker om han går
            self.standing = False #eller om han står
            self.left = 0 #Retningene til spiller
            self.right = 0
            self.down = 0
            self.up = 0

        def draw(self, win):  # Bestemmer hvilken sprite og loop som skal vises
            self.hitbox = (self.x + 5, self.y + 7, 33, 40) #Synlig hitbox
#            pygame.draw.rect(win, (255,0,0), self.hitbox,2) #Kan kommenteres ut

            if self.walkCount + 1 >= 8: #Teller frames og hastigheten til byttene mellom spritene
                self.walkCount = 0

            if not (self.standing):  # Retningene som den skal gå i og koordinaene
                if self.left == 1:
                    win.blit(walkLeft[self.walkCount // 2], (self.x, self.y)) #Tegner inn bildene i vinduet (win)
                    self.walkCount += 1 #teller frames som reseter spritesene

                elif self.right == 1: #Høyre
                    win.blit(walkRight[self.walkCount // 2], (self.x, self.y))
                    self.walkCount += 1

                elif self.down == 1: #Ned
                    win.blit(walkDown[self.walkCount // 2], (self.x, self.y))
                    self.walkCount += 1

                elif self.up == 1: #Opp
                    win.blit(walkUp[self.walkCount // 2], (self.x, self.y))
                    self.walkCount += 1
            else:
                if self.right == 1: #Dersom spilleren ikke beveger seg tilbakesetter spriten til den stillestående spriten
                    win.blit(walkRight[0], (self.x, self.y))
                elif self.up == 1:
                    win.blit(walkUp[0], (self.x, self.y))
                elif self.left == 1:
                    win.blit(walkLeft[0], (self.x, self.y))
                elif self.down == 1:
                    win.blit(walkDown[0], (self.x, self.y))

        def hit(self): #Treff mellom fiende og spilleren
            for fiende in enemies: #Viser tilbake til den tomme listen | linje 761
                if self.delay == 0: #Kontrollerer at dersom enemy treffer spiller tar spiller ikke damage på en liten stund og blir slått tilbake
                    if (
                            fiende.x + 10 < self.x < fiende.x + fiende.width - 15 or fiende.x + 10 < self.x + self.width < fiende.x + fiende.width - 15) and (
                            fiende.y + 5 < self.y < fiende.y + fiende.height - 10 or fiende.y + 5 < self.y + self.height < fiende.y + fiende.width - 10):
                        if self.x + self.width / 2 > fiende.x + fiende.width / 2:
                            if self.x < s_width - self.width - 150:
                                self.x += 100
                            else:
                                self.x = s_width - self.width - 50
                        elif self.x + self.width / 2 < fiende.x + fiende.width / 2:
                            if self.x > 150:
                                self.x -= 100
                            else:
                                self.x = 50

                        if self.y + self.height / 2 > fiende.y + fiende.height / 2:
                            if self.y < s_height - self.height - 100:
                                self.y += 50
                            else:
                                self.y = s_height - self.height - 50
                        elif self.y + self.height / 2 < fiende.y + fiende.height / 2:
                            if self.y > 100:
                                self.y -= 50
                            else:
                                self.y = 50
                        self.delay = 27

        def special(self): #Definerer spesialangrepet med delay
            fireballs.append(fireball())
            global special_delay
            if getpo: #Styrer cooldown på spesialangrepet før og etter powerup1
                special_delay = 270
            else:
                special_delay = 135


    class rom(object): #Klasse for minimappet som viser hvilket rom man er i, om døren er åpen og hvilken dør som kan åpnes
        def __init__(self, koordinat, rooms):
            self.x = koordinat[0]
            self.y = koordinat[1]
            self.rooms = rooms
            self.width = 1000 / 7
            self.height = 500 / 7
            self.border_width = 25 / 7
            self.doors = {"TOP": False,
                          "LEFT": False,
                          "RIGHT": False,
                          "BOT": False}
            if self.rooms == 0 or self.rooms == 1:
                self.doors["TOP"] = True

            if self.rooms == 1 or self.rooms == 6 or self.rooms == 7:
                self.doors["LEFT"] = True

            if self.rooms == 1 or self.rooms == 3 or self.rooms == 4:
                self.doors["RIGHT"] = True

            if self.rooms == 0:
                self.doors["BOT"] = True

        def draw(self): #Tegner rommene og dørene med fargesymbolene
            global color
            pygame.draw.rect(win, (255, 0, 0), (
            self.x + self.border_width, self.y + self.border_width, self.width - self.border_width * 2,
            self.height - self.border_width * 2), 2)
            if self.doors["TOP"]:
                if self.rooms == 0:
                    dør_farge(door1, key1)
                else:
                    dør_farge(door2, key2)

                pygame.draw.rect(win, (color), (self.x + self.width / 2 - 50 / 7, self.y - 2, 100 / 7, 5))

            if self.doors["RIGHT"]:
                if self.rooms == 1:
                    dør_farge(door3, key3)

                elif self.rooms == 3:
                    dør_farge(door4, key4)

                elif self.rooms == 4:
                    dør_farge(door5, key5)

                pygame.draw.rect(win, (color), (self.x + self.width - 2, self.y + self.height / 2 - 50 / 7, 5, 100 / 7))

            if self.doors["LEFT"]:
                if self.rooms == 1:
                    dør_farge(door6, key6)

                elif self.rooms == 6:
                    dør_farge(door7, key7)

                else:
                    dør_farge(door8, key8)
                pygame.draw.rect(win, (color), (self.x - 2, self.y + self.height / 2 - 50 / 7, 5, 100 / 7))

            if self.doors["BOT"]:
                dør_farge(door9, key9)
                pygame.draw.rect(win, (color), (self.x + self.width / 2 - 50 / 7, self.y + self.height - 2, 100 / 7, 5))

    class fireball(object):
        def __init__(self):
            self.x = man.x + man.width / 2
            self.y = man.y + man.height / 2
            self.sx = self.x - 3
            self.sy = self.y - 3
            self.swidth = 7
            self.sheight = 7
            self.xdistance = 0
            self.ydistance = 0
            self.ok = False
            self.okay = False
            for fiende in enemies:
                fiende.already_hit_fire = False

        def move(self):
            if self.ok == False:

                if self.x > 500:
                    self.xdistance -= (self.x - 500) / (27 * 2)
                elif self.x < 500:
                    self.xdistance += (500 - self.x) / (27 * 2)
                self.ok = True

            if self.okay == False:
                if self.y > 250:
                    self.ydistance -= (self.y - 250) / (27 * 2)
                elif self.y < 250:
                    self.ydistance += (250 - self.y) / (27 * 2)
                self.okay = True

            self.x += self.xdistance
            self.y += self.ydistance
            self.sx += self.xdistance
            self.sy += self.ydistance
            # print(self.xdistance, self.ydistance)
            for fiende in enemies:
                if not (fiende.already_hit_fire):
                    if fiende.x <= self.sx <= fiende.x + fiende.width or fiende.x <= self.sx + self.swidth <= fiende.x + fiende.width:
                        if fiende.y <= self.sy <= fiende.y + fiende.height or fiende.y <= self.sy + self.sheight <= fiende.y + fiende.height:
                            fiende.health -= damage
                            fiende.already_hit_fire = True

        def draw(self):
            # pygame.draw.circle(win, (255, 0, 0), (round(self.x), round(self.y)), 10, 2)
            # pygame.draw.rect(win, (0, 255, 0), (round(self.sx), round(self.sy), round(self.swidth), round(self.sheight)))
            fireball_bilde = pygame.image.load("Fireball.png")
            win.blit(fireball_bilde, (self.x - 5, self.y - 5))


        def special(self):
            if 495 < self.x < 505 and 245 < self.y < 255:
                fireballs.remove(self)
                specials.append(special_attack())


    class special_attack(object):
        def __init__(self):
            # self.x = 490
            # self.y = 245
            # self.width = 20
            # self.height = 10
            self.x = 500
            self.y = 250
            self.radius = 10
            self.ready = False
            for fiende in enemies:
                fiende.already_hit = False

        def move(self):
            # self.x -= 20
            # self.width += 40
            # self.y -= 10
            # self.height += 20
        #    for fiende in enemies:
        #         if not (fiende.already_hit):
        #             if self.x <= fiende.x <= self.x + self.width or self.x <= fiende.x + fiende.width <= self.x + self.width:
        #                 if self.y <= fiende.y <= self.y + self.height or self.y <= fiende.y + fiende.height <= self.y + self.height:
        #                     fiende.health -= damage*3
        #                     fiende.already_hit = True
        #     if 0 > self.x or self.x + self.width > s_width or 0 > self.y or self.y + self.height > s_height:
        #         specials.remove(self)
        #
        # def draw(self):
        #     pygame.draw.rect(win, (0, 255, 0), (self.x, self.y, self.width, self.height), 2)
            self.radius += 10
            for fiende in enemies:
            #     if self.x + self.radius > fiende.x:
            #         if self.y + self.radius > fiende.y:
            #             if self.x - self.radius < fiende.x + fiende.width:
            #                 if self.y - self.radius > fiende.y + fiende.height:
            #                     fiende.health -= damage*3
            #                     fiende.already_hit = True
                if not(fiende.already_hit):
                    if (fiende.y + fiende.height) > self.y - self.radius and fiende.x + fiende.width > self.x - self.radius and fiende.x < self.x + self.radius:
                        fiende.health -= damage*2
                        fiende.already_hit = True
            if self.radius >= 500:
                specials.remove(self)
        def draw(self):
            pygame.draw.circle(win, (200, 0, 0), (round(self.x), round(self.y)), self.radius, 2)

    class knife(object): #Klasse for knivkastingen
        def __init__(self): #Variabbler for kniven
            self.radius = 10
            self.retning = retning
            self.vel = 15
            self.width = 10
            self.height = 10
            self.delay = 0
            if man.left == 1: #Viser til retningen mannen har og overfører den til kniven
                self.retning = 1
                self.x = man.x - 10
                self.y = man.y + 20
            elif man.right == 1:
                self.retning = 2
                self.x = man.x + man.width + 10
                self.y = man.y + 20
            elif man.up == 1:
                self.retning = 4
                self.x = man.x + man.width / 2
                self.y = man.y - 10
            else:
                self.retning = 3
                self.x = man.x + man.width / 2
                self.y = man.y + man.height + 10

        def draw(self, win): #Tegner kniven i forhold til retningen mannen retning da han kastet den
            if self.retning == 1:
                kniv = pygame.image.load("KnivV.png") #Venstre
                win.blit(kniv, (self.x, self.y))
            elif self.retning == 2:
                kniv = pygame.image.load("KnivH.png") #Høre
                win.blit(kniv, (self.x, self.y))
            elif self.retning == 3:
                kniv = pygame.image.load("KnivN.png") #Ned
                win.blit(kniv, (self.x, self.y))
            elif self.retning == 4:
                kniv = pygame.image.load("KnivO.png") #Opp
                win.blit(kniv, (self.x, self.y))

        def move(self): #Bevegelsen for kniven
            if self.retning == 1: #Venstre
                if self.x <= 0: #Dersom x er mindre enn 0 slet kniven fra listen
                    kniver.pop(kniver.index(self))
                    pass
                else:
                    self.x -= self.vel #Bevegelsefarten til kniven
                    pass

            if self.retning == 2: #Høyre
                if self.x >= s_width: #Dersom x er større enn bredden til skjermen
                    kniver.pop(kniver.index(self))
                    pass
                else:
                    self.x += self.vel #Bevegelsefarten til kniven
                    pass

            if self.retning == 3: #Ned
                if self.y >= s_height: #Dersom y er større enn høyden til skjermen
                    kniver.pop(kniver.index(self))
                    pass
                else:
                    self.y += self.vel #Bevegelsefarten til kniven
                    pass

            if self.retning == 4: #Opp
                if self.y <= 0: #Dersom y er mindre enn 0
                    kniver.pop(kniver.index(self)) 
                    pass
                else:
                    self.y -= self.vel #Bevegelsefarten til kniven
                    pass


    class key(object): #klasse for nøklene
        def __init__(self, color, x, y, width, height): #Variablene til nøkklene
            self.x = x
            self.y = y
            self.color = color
            self.height = height
            self.width = width
            self.show = False #Skal kniven vises?
            self.open = False #Har kniven åpnet døren?
            self.hitbox = (self.x, self.y, self.width, self.height)

        def draw(self, win): #Tegner inn nøkkelen
            nøkkel = pygame.image.load("Nøkkel.png")
            win.blit(nøkkel, (self.x, self.y))

    class doorUp(object): #Tegner dørene som peker opp eller ned
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.width = 100 #Størrelse
            self.height = 10
            self.color = (150, 75, 0)
            self.locked = True

        def draw(self, win):
            pygame.draw.rect(win, (self.color), (self.x, self.y, self.width, self.height)) #Tegner inn et rektangel med forhåndsbesteme verdier | Linje 809, 810 og 817


    class doorSide(object): #Tegnerdørene som peker høyre eller venstre
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.width = 10 #Størrelse
            self.height = 100
            self.color = (150, 75, 0)
            self.locked = True

        def draw(self, win):
            pygame.draw.rect(win, (self.color), (self.x, self.y, self.width, self.height))  #Tegner inn et rektangel med forhåndsbesteme verdier | Linje 811-816


    class hjerte(object): #Klasse for fulle hjerter
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.width = 25
            self.height = 25

        def draw(self, win):
            hjerter = pygame.image.load("Hjerte.png") #Tegner inn hjertene
            win.blit(hjerter, (self.x, self.y))


    class tomhjerte(object): #Klasse for tomme hjerter
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.width = 25
            self.height = 25

        def draw(self, win):
            tomhjerter = pygame.image.load("HjerteTom.png") #Tegner inn hjertene
            win.blit(tomhjerter, (self.x, self.y))


    class power(object): #Klasse for powerup 1
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def draw(self, win):
            powerup = pygame.image.load("PowerUp.png") #Tegner inn powerup1
            win.blit(powerup, (self.x, self.y))


    class damageicon(object): #Klasse for powerup 2
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def draw(self, win):
            powerup2 = pygame.image.load("DamageUp.png") #Tegner inn powerup2
            win.blit(powerup2, (self.x, self.y))

    #Variaber for om du kan få power-upen 
    gethe = True #få hjerter
    getpo = True #få powerup 1
    getda = True #få powerup 2


    class chest(object): #Klasse for kistene
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.open = False
            self.width = 25
            self.height = 25

        def draw(self, win): #Tegner inn kistene 
            if self.open == False: #Dersom kisten ikke er åpen tegner inn lukket kiste
                kiste = kister[0]
                win.blit(kiste, (self.x, self.y))
            elif self.open == True: #Dersom kisten er åpen tegner inn åpen kiste
                kiste = kister[1]
                win.blit(kiste, (self.x, self.y))


    class enemy(object): #klasse for fienden
        def __init__(self, x, y, width, height, vel, health): #Definerer viktige variabler
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.vel = vel
            self.health = health
            self.already_hit = False
            self.already_hit_fire = False

        def search(self):
            pass

        def draw(self):
            if room == 7 or room == 8 or room == 9: #tegner inn en annen farget sprite dersom room = 7/8/9
                enemy = icespirit[enemy_delay // 10]
            else:
                enemy = firespirit[enemy_delay // 10]
            
            win.blit(enemy, (self.x, self.y)) #Tegner inn enemien
            pygame.draw.rect(win, (255, 0, 0), (self.x + 5, self.y - 15, 54, 10))  # Rød healthbar
            pygame.draw.rect(win, (0, 255, 0), (self.x + 5, self.y - 15, self.health, 10))  # Grønn healthbar

#            pygame.draw.rect(win, (0,200,0), (self.x + 5, self.y + 5, self.width, self.height), 2) #Hitboks til enemies

        def move(self): #Bevegelsen til fienden
            #Bevegelse mot mannen, retning høyre og venstre (x)
            if man.y + 25 < self.y < man.y + man.height - 25 or man.y + 25 < self.y + self.height < man.y + man.height - 25 or man.y < self.y + self.height / 2 < man.y + man.height:
                if self.x < man.x:
                    self.x += self.vel
                else:
                    self.x -= self.vel
            #Bevegelse mot mannen, retning opp og ned (y)
            elif man.x + 25 < self.x < man.x + man.width - 25 or man.x + 25 < self.x + self.width < man.x + man.width - 25 or man.x < self.x + self.width / 2 < man.x + man.width:
                if self.y < man.y:
                    self.y += self.vel
                else:
                    self.y -= self.vel

            else: #
                if self.x + self.width / 2 < man.x + (man.width / 2) and self.y + self.height / 2 < man.y + (
                        man.height / 2):
                    self.x += (self.vel ** 2 / 2) ** 0.5 #Bruker pytagoras til å bestemme hvordan man skal gå i forhold til spiller
                    self.y += (self.vel ** 2 / 2) ** 0.5 #Går skrått
                elif self.x + self.width / 2 < man.x + (man.width / 2) and self.y + self.height / 2 > man.y + (
                        man.height / 2):
                    self.x += (self.vel ** 2 / 2) ** 0.5
                    self.y -= (self.vel ** 2 / 2) ** 0.5
                elif self.x + self.width / 2 > man.x + (man.width / 2) and self.y + self.height / 2 < man.y + (
                        man.height / 2):
                    self.x -= (self.vel ** 2 / 2) ** 0.5
                    self.y += (self.vel ** 2 / 2) ** 0.5
                elif self.x + self.width / 2 > man.x + (man.width / 2) and self.y + self.height / 2 > man.y + (
                        man.height / 2):
                    self.x -= (self.vel ** 2 / 2) ** 0.5
                    self.y -= (self.vel ** 2 / 2) ** 0.5


    class Boss(object): #Klasse for bossen
        def __init__(self, x, y, height, width, health): #Defienerer variabler for Boss
            self.x = x
            self.y = y
            self.height = height
            self.width = width
            self.health = health
            self.atkpattern = 0
            self.hitbox = (self.x, self.y, self.width, self.height)
            self.starthealth = health

        def search(self): #Søker plasseringen til mannen
            self.manplacement = 0
            for i in range(1, 6):
                if s_start_x + x_zone * i <= man.x + man.width / 2 <= s_end_x - x_zone * i: #Bruker forhåndsbestemte områder og sjekker om mannen er i disse sonene
                    if s_start_y + y_zone * (i - 1) <= man.y + man.height / 2 <= s_start_y + y_zone * i:
                        self.newmanplacement = "N"
                    if s_end_y - y_zone * (i - 1) >= man.y + man.height / 2 >= s_end_y - y_zone * i:
                        self.newmanplacement = "S"
                if s_start_y + y_zone * (i - 1) <= man.y + man.height / 2 <= s_end_y - y_zone * (i - 1):
                    if s_start_x + x_zone * (i - 1) <= man.x + man.width / 2 <= s_start_x + x_zone * i:
                        self.newmanplacement = "W"
                    if s_end_x - x_zone * (i - 1) >= man.x + man.width / 2 >= s_end_x - x_zone * i:
                        self.newmanplacement = "E"

            if self.newmanplacement == self.manplacement: #sjekker om hvor mannen beveger seg ved å sjekke om han er i den samme sonen
                reset_delay()
            self.manplacement = self.newmanplacement

            self.attack() #Angrep, definert under

        def attack(self): #Angrep
            global boss_delay_attack
            if self.atkpattern == 1: #Tre angrepsmønstre | Her 1
                projectiles.append(Boss_projectiles(self.manplacement, self.atkpattern, 0)) # Røde firkanter i en retning VHON
                
            elif self.atkpattern == 2: #Angrepsmønster 2 | Skyter ut bommerangene 
                
                if boss_delay_attack == 0:
                    for nummer in range(6):
                        projectiles.append(Boss_projectiles(self.manplacement, self.atkpattern, nummer))
                        boss_delay_attack = 9
                    


        def draw(self): #Tegner bossen
            MB = pygame.image.load("Boss.png") #Tegner bossen 

            global Bosses
            if Bosses:
                if self.health < 1: #Dersom bossens liv er null bytt spriten til tom
                    MB = pygame.image.load("Tom.png")
            win.blit(MB, (self.x, self.y))
            if self.health > 400: #Farger healthbaren forskjellig i forhold til mengde liv igjen
                color = pygame.Color("green")

            elif self.health > 200:
                color = pygame.Color("yellow")

            else:
                color = pygame.Color("red")
            
            pygame.draw.rect(win, (180,180,180), (200, 5, self.starthealth, 10)) #Tegner inn bakgrunn for healthbaren
            pygame.draw.rect(win, color, (200, 5, self.health, 10)) #tegner inn faktisk health
            for x in range(200, 601, 200):
                pygame.draw.rect(win, (0,0,0), (x, 5, self.starthealth/3, 10), 2) #tegner inn tre deler av healthbar

        def spawn(): #Styrer spawn funksjonenen til enemies til klassen enemy
            global telle
            telle = True
            global antall
            antall = 2
        
        def move(self):
            pass


    class Boss_projectiles(object): #Klassen for projektilene til bossen
        def __init__(self, retning, atkpattern, nummer): #Definerer variabler 
            self.vel = 7
            self.retning = retning
            self.atkpattern = atkpattern #sjekker angrepsmønsteret
            self.nummer = nummer
            self.hjørne = hjørne_koordinater[self.retning][self.nummer] #sjekker hjørnene

            if self.atkpattern == 1: #Sjekker koordinatene til retningen projektilene skal ha mot
                self.koordinat = koordinater[self.retning]
                self.width = self.koordinat[2]
                self.height = self.koordinat[3]
            elif self.atkpattern == 2:
                self.koordinat = koordinater[self.hjørne]
                self.vel *= 2
            self.x = self.koordinat[0]
            self.y = self.koordinat[1]

            if self.atkpattern == 2 and (self.nummer == 1 or self.nummer == 4):
                self.height = 15
                self.width = 15
            elif self.atkpattern == 2:
                self.square_x = self.koordinat[0] - 3.5
                self.square_y = self.koordinat[1] - 3.5
                self.square_width = 7
                self.square_height = 7

        def draw(self): #tegner inn projektilene
            global Bosses
            if Bosses:
                if self.atkpattern == 1 and Main_Boss.health > 1:
                    pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.height)) #Et rød rektangel
                elif self.atkpattern == 2 and (self.nummer == 1 or self.nummer == 4) and Main_Boss.health > 1:
                    bilde = pygame.image.load("Boomerang" + self.hjørne + ".png") #Boomerangen mot sidene
                    #bilde = pygame.image.load("BoomerangTR.png")
                    win.blit(bilde, (self.x, self.y))
                    #pygame.draw.rect(win, (0, 255, 0), (self.x, self.y, self.width, self.height))
                elif self.atkpattern == 2 and Main_Boss.health > 1: #Blå sirkler
                    pygame.draw.circle(win, (0, 0, 255), (round(self.x), round(self.y)), 5)

        def move(self): #Bevegelsen til projektilene
            if self.atkpattern == 1:
                if self.retning == "N": #Dersom retningen er Nord
                    self.y -= self.vel / 2 #Øker y verdien med halvparten av hastigheten for at de ikke skal klumpe seg opp
                elif self.retning == "S": #Retning Sør
                    self.y += self.vel / 2 #likt som linjen to over
                elif self.retning == "W": #Retning West
                    self.x -= self.vel #Endre x med hastigheten til projektilen
                elif self.retning == "E": #Retning East
                    self.x += self.vel #Endre x med haastigheten til projektilen

            elif self.atkpattern == 2: 
                if self.hjørne == "TR": #Retning TopRight
                    self.x += (self.vel / 2) ** 0.5 #Beveger projektilen skrått med kvadratroten av hastighet delt på to 
                    self.y -= (self.vel / 2) ** 0.5
                elif self.hjørne == "TL": #Retning TopLeft
                    self.x -= (self.vel / 2) ** 0.5
                    self.y -= (self.vel / 2) ** 0.5
                elif self.hjørne == "BR": #Retning BottomRight
                    self.x += (self.vel / 2) ** 0.5
                    self.y += (self.vel / 2) ** 0.5
                elif self.hjørne == "BL": #Retning BotttomLeft
                    self.x -= (self.vel / 2) ** 0.5
                    self.y += (self.vel / 2) ** 0.5
                elif self.hjørne == "TBR": #Retning TopBottomRight
                    self.x += 2 * ((self.vel / 3) ** 0.5) #Beveger projektilen skrått mot den nedre delen av top right 
                    self.square_x += 2 * ((self.vel / 3) ** 0.5)
                    self.y -= ((self.vel / 3) ** 0.5)
                    self.square_y -= ((self.vel / 3) ** 0.5)
                elif self.hjørne == "TTR": #Retning TopTopRight
                    self.x += ((self.vel / 3) ** 0.5)
                    self.y -= 2 * ((self.vel / 3) ** 0.5)
                    self.square_x += ((self.vel / 3) ** 0.5)
                    self.square_y -= 2 * ((self.vel / 3) ** 0.5)
                elif self.hjørne == "TBL": #Retning TopBottomLeft
                    self.x -= 2 * ((self.vel / 3) ** 0.5)
                    self.y -= ((self.vel / 3) ** 0.5)
                    self.square_x -= 2 * ((self.vel / 3) ** 0.5)
                    self.square_y -= ((self.vel / 3) ** 0.5)
                elif self.hjørne == "TTL": #Retning TopTopLeft
                    self.x -= ((self.vel / 3) ** 0.5)
                    self.y -= 2 * ((self.vel / 3) ** 0.5)
                    self.square_x -= ((self.vel / 3) ** 0.5)
                    self.square_y -= 2 * ((self.vel / 3) ** 0.5)
                elif self.hjørne == "BTR": #BottomTopRight
                    self.x += 2 * ((self.vel / 3) ** 0.5)
                    self.y += ((self.vel / 3) ** 0.5)
                elif self.hjørne == "BBR": #BottomBottomRight
                    self.x += ((self.vel / 3) ** 0.5)
                    self.y += 2 * ((self.vel / 3) ** 0.5)
                    self.square_x += ((self.vel / 3) ** 0.5)
                    self.square_y += 2 * ((self.vel / 3) ** 0.5)
                elif self.hjørne == "BTL": #BottomTopLeft
                    self.x -= 2 * ((self.vel / 3) ** 0.5)
                    self.y += ((self.vel / 3) ** 0.5)
                    self.square_x -= 2 * ((self.vel / 3) ** 0.5)
                    self.square_y += ((self.vel / 3) ** 0.5)
                elif self.hjørne == "BBL": #BottomBottomLeft
                    self.x -= ((self.vel / 3) ** 0.5)
                    self.y += 2 * ((self.vel / 3) ** 0.5)
                    self.square_x -= ((self.vel / 3) ** 0.5)
                    self.square_y += 2 * ((self.vel / 3) ** 0.5)

        def hit(self): #Definerer kollisjon mellom projektilene og spiller
            global man_hit_delay
            if self.atkpattern == 1 or self.atkpattern == 2 and (self.nummer == 1 or self.nummer == 4):
                if man.x <= self.x <= man.x + man.width or man.x <= self.x + self.width <= man.x + man.width: #Registrerer treff ved  sjekke x og y koordinatene til spiller og projektilene
                    if man.y <= self.y <= man.y + man.height or man.y <= self.y + self.height <= man.y + man.height:
                        if man_hit_delay == 0: #Skaper et delay mellom treffene 
                            projectiles.remove(projectile)
                            man.health -= 1
                            man_hit_delay = 27
                elif s_start_x >= self.x or s_end_x <= self.x + self.width: #Sletter projektilene dersom de når kantene (x)
                    projectiles.remove(projectile)
                elif s_start_y >= self.y or s_end_y <= self.y + self.height: #Sletter projektilene dersom de når kantene (y)
                    projectiles.remove(projectile)
            
            elif self.atkpattern == 2: #samme som over men med angrepsmønster 2
                if man.x <= self.square_x <= man.x + man.width or man.x <= self.square_x + self.square_width <= man.x + man.width:
                    if man.y <= self.square_y <= man.y + man.height or man.y <= self.square_y + self.square_height <= man.y + man.height:
                        if man_hit_delay == 0:
                            projectiles.remove(projectile)
                            man.health -= 1
                            man_hit_delay = 27
                elif s_start_x >= self.square_x or s_end_x <= self.square_x + self.square_width:
                    projectiles.remove(projectile)
                elif s_start_y >= self.square_y or s_end_y <= self.square_y + self.square_height:
                    projectiles.remove(projectile)


    enemies = [] #Tom liste som brukes for å legge enemies i
    boss = [] #Tom liste for bossen
    win_color = ((255, 255, 255))  # Bakgrunnsfarge i rom 1

    random1 = random.randint(100, 900) #Spawnkoordinater for enemies
    random2 = random.randint(100, 400)
    random3 = random.randint(100, 900)
    random4 = random.randint(100, 400)

    man = player(460, 220, 40, 45, 3)  # Informasjon om spiller x, y, width, height, health

    liv1 = hjerte(30, 30) #Definerer hjertene og deres tomhjertede-motpart
    tomliv1 = tomhjerte(30, 30)
    liv2 = hjerte(50, 30)
    tomliv2 = tomhjerte(50, 30)
    liv3 = hjerte(70, 30)
    tomliv3 = tomhjerte(70, 30)
    liv4 = hjerte(90, 30)

    powerUp = power(900, 30) #powerup1

    damageUp = damageicon(830, 30) #powerup2

    kiste1 = chest(470, 220) #kistene (rom3)
    kiste2 = chest(470, 220) #kistene (rom6)
    kiste3 = chest(470, 220) #kistene (rom9)

    key1 = key((255, 0, 0), random1, random2, 30, 17)  # Verdiene til nøklene på de forskjellige verdene
    key2 = key((255, 0, 0), random3, random4, 30, 17)  # Nøklene for de forskjellige rommene
    key3 = key((255, 0, 0), random1, random2, 30, 17)
    key4 = key((255, 0, 0), random3, random4, 30, 17)
    key5 = key((255, 0, 0), random1, random2, 30, 17)
    key6 = key((255, 0, 0), random3, random4, 30, 17)
    key7 = key((255, 0, 0), random1, random2, 30, 17)
    key8 = key((255, 0, 0), random3, random4, 30, 17)
    key9 = key((255, 0, 0), random1, random2, 30, 17)  # Lage en nøkkel som ser mer spess ut som er for bossen!

    key1.open = False #Variabler som sjekker om døren er åpen
    key2.open = False
    key3.open = False
    key4.open = False
    key5.open = False
    key6.open = False
    key7.open = False
    key8.open = False
    key9.open = False



    door1 = doorUp(s_width / 2 - 50, 0)  # Plasseringen til dørene på skjermen
    door2 = doorUp(s_width / 2 - 50, 0)
    door3 = doorSide(s_width - 10, s_height / 2 - 50)
    door4 = doorSide(s_width - 10, s_height / 2 - 50)
    door5 = doorSide(s_width - 10, s_height / 2 - 50)
    door6 = doorSide(0, s_height / 2 - 50)
    door7 = doorSide(0, s_height / 2 - 50)
    door8 = doorSide(0, s_height / 2 - 50)
    door9 = doorUp(s_width / 2 - 50, s_height - 10)

    door1.locked = True #Variabler for å sjekke om døren er låst eller åpen
    door2.locked = True
    door3.locked = True
    door4.locked = True
    door5.locked = True
    door6.locked = True
    door7.locked = True
    door8.locked = True
    door9.locked = True


    s_end_x = 1000
    s_end_y = 500
    s_start_x = 0
    s_start_y = 0
    Bosses = False
    delay = 0
    telle = True
    antall = 1


    def redraw_minimap(): #Funksjon som tegner minimapet 
        global rooms, room, cords 
        if len(cords) == 0:
            x_linjer = [] 
            y_linjer = []
            for x in range(7):
                x_linjer.append((1000 / 7) * x) #Linjene til rommene

            for x in range(4):
                y_linjer.append(((500 / 7) * x) + 100)

            coordinates = [] #Koordintatene til rommene i mappet
            coordinates.append((x_linjer[3], y_linjer[0]))
            for x in range(7):
                coordinates.append((x_linjer[x], y_linjer[1]))
            coordinates.append((x_linjer[3], y_linjer[2]))
            coordinates.append((x_linjer[3], y_linjer[3]))

            cords = [] #Koordinatene til rommene sortert
            cords.append(coordinates[-2])
            cords.append(coordinates[4])
            cords.append(coordinates[0])
            for x in range(5, 8):
                cords.append(coordinates[x])
            for x in range(3, 0, -1):
                cords.append(coordinates[x])
            cords.append(coordinates[-1])

        for x in range(10):
            rooms.append(rom(cords[x], x))
        win.fill((0, 0, 0))
        win.blit(pygame.image.load("minimap_symboler_forminsket.png"), (10, (1000/7)*2)) #Importerer info-bilde
        pygame.draw.rect(win, (0,0,0), (10, (1000/7)*2 + 150, 200, 100))
        for romm in rooms:
            romm.draw()

        ekstra_cords = cords[room-1]
        pygame.draw.circle(win, pygame.Color("green"), (round(ekstra_cords[0] + (man.x + man.width/2)/7), round(ekstra_cords[1] + (man.y + man.height/2)/7)), 5, 2) #Drawer spiller i map
        for fiende in enemies:
            pygame.draw.circle(win, pygame.Color("red"), (round(ekstra_cords[0] + (fiende.x + fiende.width / 2) / 7),round(ekstra_cords[1] + (fiende.y + fiende.height / 2) / 7)), 2) #Drawer enemies i map
        
        pygame.display.update() #Oppdaterer skjermen


    def dør_farge(dør, nøkkel): #Fargene på døren på minimapet (blå/hvite)
        global color
        if dør.locked and nøkkel.open: #Dersom døren er låst, men du kan åpne den
            color = pygame.Color("blue")
        elif not dør.locked: #Dersom døren er åpnet
            color = pygame.Color("white")
        elif not nøkkel.open: #Dersom døren er låst
            color = (150, 75, 0)


    def enemy_create(antall): #lager enemies
        global telle
        if telle: #Telle er variablen som bestemmer om det kan spawne enemies
            for z in range(antall):
                okay = False
                while not okay: #Styrer spawnpointene så enemiene ikke spawner på hverandre
                    not_okay = False
                    if room == 1:
                        enemy_x = 50
                        enemy_y = 50
                    else:
                        enemy_x = random.choice(spawnx)
                        enemy_y = random.choice(spawny)
                    for fiende in enemies:
                        if enemy_x == fiende.x and enemy_y == fiende.y:
                            not_okay = True
                    if not (not_okay):
                        okay = True
                enemies.append(enemy(enemy_x, enemy_y, 40, 50, 3, 54)) #Legger til enemies i listen
            telle = False #Stopper spawningen av enemies

    drepte_enemies = 0 #Teller antall drepte enemies


    def redrawGamewindow(): #Hovedtegne definisjon
        global win_color
        global bg
        global kastespeed
        win.fill(win_color) #Tegner bakgrunnen
        win.blit(bg, (0, 0))


        enemy_create(antall)
        global drepte_enemies 
        for fiende in enemies:
            if fiende.health <= 0:
                enemies.remove(fiende) #sletter enemies og øker antall drepte enemies med 1
                drepte_enemies += 1
        for firebal in fireballs: #tegner fireball i fireballs listen
            firebal.draw()
        for spec in specials: #Tegner specialangrep i specials listen
            spec.draw()
        for fiende in enemies: #Tegner enemy i enemies listen
            fiende.draw()

        for kniv in kniver: #Tegner kniver 
            knife.draw(kniv, win)

        if room == 3 and kiste1.open == True: #Tegner kisten om den er åpen
            kiste1.draw(win)
        elif room == 3 and kiste1.open == False and len(enemies) == 0: #Tegner kisten dersom det ikke er noen enemies og den ikke er åpen
            kiste1.draw(win)

        if room == 6 and kiste2.open == True and len(enemies) == 0: #samme som over men annet rom
            kiste2.draw(win)
        elif room == 6 and kiste2.open == False and len(enemies) == 0:
            kiste2.draw(win)

        if room == 9 and kiste3.open == True and len(enemies) == 0:
            kiste3.draw(win)
        elif room == 9 and kiste3.open == False and len(enemies) == 0:
            kiste3.draw(win)

        if kiste2.open == True: #Tegner powerup1
            powerUp.draw(win)

        if kiste3.open == True: #Tegner powerup2
            damageUp.draw(win)

        for projectile in projectiles: #Tegner bossprojektilene
            projectile.draw()
        if dont_draw != True: #Tegner spilleren
            man.draw(win)

        if man.health == 3: #Tegner mengden liv
            liv1.draw(win)
            liv2.draw(win)
            liv3.draw(win)
        elif man.health == 2:
            liv1.draw(win)
            liv2.draw(win)
            tomliv3.draw(win)
        elif man.health == 1:
            liv1.draw(win)
            tomliv2.draw(win)
            tomliv3.draw(win)
        elif man.health == 4:
            liv1.draw(win)
            liv2.draw(win)
            liv3.draw(win)
            liv4.draw(win)

        if room == 1: #Tegner inn "plattformene"/borderene som stopper spilleren fra å bevege seg ut
            platform(0, 0, 25, s_height)
            platform(s_width - 25, 0, 25, s_height)
            platform(s_width / 2 + 50, 0, s_width / 2 - 50, 25)
            platform(0, 0, s_width / 2 - 50, 25)
            platform(s_width / 2 + 50, s_height - 25, s_width / 2 - 50, 25)
            platform(0, s_height - 25, s_width / 2 - 50, 25)
            win_color = (255, 255, 255)
            if door9.locked:
                door9.draw(win) #Tegner dørene og nøklene
            if door1.locked:
                door1.draw(win)
            if key1.show:
                key1.draw(win)
        if room == 2: #Likt som room = 1 | Linje 980
            platform(s_width / 2 + 50, 0, s_width / 2 - 50, 25)
            platform(0, 0, s_width / 2 - 50, 25)
            platform(s_width / 2 + 50, s_height - 25, s_width / 2 - 50, 25)
            platform(0, s_height - 25, s_width / 2 - 50, 25)
            platform(s_width - 25, 0, 25, s_height / 2 - 50)
            platform(s_width - 25, s_height / 2 + 50, 25, s_height / 2 - 50)
            platform(0, 0, 25, s_height / 2 - 50)
            platform(0, s_height / 2 + 50, 25, s_height / 2 - 50)

            win_color = (128, 128, 128)
            if door6.locked:
                door6.draw(win)
            if door2.locked:
                door2.draw(win)
            if door3.locked:
                door3.draw(win)
            if key2.show:
                key2.draw(win)
        if room == 3:
            platform(0, 0, 25, s_height)
            platform(s_width - 25, 0, 25, s_height)
            platform(0, 0, s_width, 25)
            platform(0, s_height - 25, s_width / 2 - 50, 25)
            platform(s_width / 2 + 50, s_height - 25, s_width / 2 - 50, 25)

            win_color = (200, 128, 24)
            if key3.show:
                key3.draw(win)
        if room == 4:
            platform(0, 0, s_width, 25)
            platform(0, s_height - 25, s_width, 25)
            platform(s_width - 25, 0, 25, s_height / 2 - 50)
            platform(s_width - 25, s_height / 2 + 50, 25, s_height / 2 - 50)
            platform(0, 0, 25, s_height / 2 - 50)
            platform(0, s_height / 2 + 50, 25, s_height / 2 - 50)

            win_color = (200, 100, 100)
            if door4.locked:
                door4.draw(win)
            if key4.show:
                key4.draw(win)
        if room == 5:
            platform(0, 0, s_width, 25)
            platform(0, s_height - 25, s_width, 25)
            platform(s_width - 25, 0, 25, s_height / 2 - 50)
            platform(s_width - 25, s_height / 2 + 50, 25, s_height / 2 - 50)
            platform(0, 0, 25, s_height / 2 - 50)
            platform(0, s_height / 2 + 50, 25, s_height / 2 - 50)
            win_color = (100, 200, 100)
            if door5.locked:
                door5.draw(win)
            if key5.show:
                key5.draw(win)
        if room == 6:
            platform(0, 0, s_width, 25)
            platform(0, s_height - 25, s_width, 25)
            platform(s_width - 25, 0, 25, s_height)
            platform(0, 0, 25, s_height / 2 - 50)
            platform(0, s_height / 2 + 50, 25, s_height / 2 - 50)

            win_color = (0, 0, 0)
            if key6.show:
                key6.draw(win)
        if room == 7:
            platform(0, 0, s_width, 25)
            platform(0, s_height - 25, s_width, 25)
            platform(s_width - 25, 0, 25, s_height / 2 - 50)
            platform(s_width - 25, s_height / 2 + 50, 25, s_height / 2 - 50)
            platform(0, 0, 25, s_height / 2 - 50)
            platform(0, s_height / 2 + 50, 25, s_height / 2 - 50)

            win_color = (0, 200, 200)
            if door7.locked:
                door7.draw(win)
            if key7.show:
                key7.draw(win)
        if room == 8:
            platform(0, 0, s_width, 25)
            platform(0, s_height - 25, s_width, 25)
            platform(s_width - 25, 0, 25, s_height / 2 - 50)
            platform(s_width - 25, s_height / 2 + 50, 25, s_height / 2 - 50)
            platform(0, 0, 25, s_height / 2 - 50)
            platform(0, s_height / 2 + 50, 25, s_height / 2 - 50)
            win_color = (200, 0, 200)
            if door8.locked:
                door8.draw(win)
            if key8.show:
                key8.draw(win)

        if room == 9:
            platform(0, 0, s_width, 25)
            platform(0, s_height - 25, s_width, 25)
            platform(s_width - 25, 0, 25, s_height / 2 - 50)
            platform(s_width - 25, s_height / 2 + 50, 25, s_height / 2 - 50)
            platform(0, 0, 25, s_height)

            win_color = (200, 200, 0)
            if key9.show:
                key9.draw(win)
        if room == 10:
            platform(0, 0, s_width, 25)
            platform(0, s_height - 25, s_width, 25)
            platform(s_width - 25, 0, 25, s_height)
            platform(0, 0, 25, s_height)

            win_color = (0, 100, 100)

        # Tegner nøkkler
        if key1.show and room == 1:
            key1.draw(win)
        if key2.show and room == 2:
            key2.draw(win)
        if key3.show and room == 3:
            key3.draw(win)
        if key4.show and room == 4:
            key4.draw(win)
        if key5.show and room == 5:
            key5.draw(win)
        if key6.show and room == 6:
            key6.draw(win)
        if key7.show and room == 7:
            key7.draw(win)
        if key8.show and room == 8:
            key8.draw(win)
        if key9.show and room == 9:
            key9.draw(win)

        # Tegner dører
        if door1.locked and room == 1:
            door1.draw(win)
        if door2.locked and room == 2:
            door2.draw(win)
        if door3.locked and room == 2:
            door3.draw(win)
        if door4.locked and room == 4:
            door4.draw(win)
        if door5.locked and room == 5:
            door5.draw(win)
        if door6.locked and room == 2:
            door6.draw(win)
        if door7.locked and room == 7:
            door7.draw(win)
        if door8.locked and room == 8:
            door8.draw(win)
        if door9.locked and room == 1:
            door9.draw(win)

        if len(enemies) == 1:
            if room == 1:
                for fiende in enemies: #Spawner nøkkelen i rommet hvor den siste enemien dør
                    key1.x = fiende.x
                    key1.y = fiende.y

            elif room == 2:
                for fiende in enemies:
                    key2.x = fiende.x
                    key2.y = fiende.y
            elif room == 3:
                for fiende in enemies:
                    key3.x = fiende.x
                    key3.y = fiende.y
            elif room == 4:
                for fiende in enemies:
                    key4.x = fiende.x
                    key4.y = fiende.y
            elif room == 5:
                for fiende in enemies:
                    key5.x = fiende.x
                    key5.y = fiende.y
            elif room == 6:
                for fiende in enemies:
                    key6.x = fiende.x
                    key6.y = fiende.y
            elif room == 7:
                for fiende in enemies:
                    key7.x = fiende.x
                    key7.y = fiende.y
            elif room == 8:
                for fiende in enemies:
                    key8.x = fiende.x
                    key8.y = fiende.y
            elif room == 9:
                for fiende in enemies:
                    key9.x = fiende.x
                    key9.y = fiende.y
       
        win.blit(pygame.image.load("KnivO.png"), (30, 55)) #Tegner ikonet for cooldown på kniv
        win.blit(pygame.image.load("Fireball.png"), (35, 90)) #Tegner ikonet for cooldown på special
        bredde = (54 / kastespeed) * knife.delay
        pygame.draw.rect(win, (0, 0, 0), (50, 65, 54, 10)) #Cooldown Kniv - tegner firkanten som er bakgrunnen
        if knife.delay > 0:
            pygame.draw.rect(win, (255, 0, 0), (50, 65, bredde, 10)) #Cooldown Kniv - tegner firkanten som er cooldownen 
        if getpo:
            bredde2 = (54 / 270) * special_delay
        else:
#            global special_delay
#            if special_delay > 135:
#                special_delay = 135
            bredde2 = (54 / 135) * special_delay
        pygame.draw.rect(win, (0, 0, 0), (50, 90, 54, 10)) #Likt som over men for special
        if special_delay > 0:
            pygame.draw.rect(win, (255, 0, 0), (50, 90, bredde2, 10)) #Likt som over men for special
        pygame.display.update()


    def reset_delay():
        global delay
        delay = 54
        Main_Boss.atkpattern = 1


    def platform(x, y, width, height): #Stopper spilleren fra å gå over borderen
        if man.y + man.height > y and man.y < y + height and man.x + man.width > x and man.x + man.width < x + 2 * man.vel:
            man.x = x - man.width  # Venstre
        elif man.y + man.height > y and man.y < y + height and man.x < x + width and man.x > x + width - man.vel * 2:
            man.x = x + width  # Høyre
        if man.y + man.height > y and man.y + man.height < y + 2 * man.vel and man.x + man.width > x and man.x < x + width:
            man.y = y - man.height  # Over
        elif man.y < y + height and man.y > y + height - man.vel * 2 and man.x + man.width > x and man.x < x + width:
            man.y = y + height  # Under
        pass


    class Button(): #Klasse for knappene 
        def __init__(self, x, y, width, height, types, color):
            self.x = x
            self.y = y
            self.height = height
            self.width = width
            self.bool = False
            self.types = types
            self.color = pygame.Color(color)
            self.selected = False
        def check(self): #Sjekker om musen er over knappen samt klikk
            global click_delay
            global mx, my
            if self.bool:
                self.bool = False
            elif not (self.bool) and click_delay == 0:
                if self.x < mx < self.x + self.width:
                    if self.y < my < self.y + self.height:
                        self.bool = True
                        self.mx = self.x - mx
                        self.my = self.y - my
                        click_delay = 3

        def select(self): #Sjekker om musen er over og selected
            if self.x < mx < self.x + self.width:
                if self.y < my < self.y + self.height:
                    self.selected = True
                else:
                    self.selected = False
            else:
                self.selected = False

        """
        Linjene under er ikke nødvendige for skriptet, men ble laget i tilfelle om vi trengte det
        """

#        def move(self): 
#            global mx, my
#            if self.bool:
#                if not(border_width > self.x or self.x > s_width - border_width) and not(border_width > self.y  or  self.y > s_height - border_width):
#                    self.x = mx + self.mx
#                    self.y = my + self.my
#                if border_width > self.x:
#                    self.x = border_width
#
#                if self.x + self.width > s_width - border_width:
#                    self.x = s_width - border_width - self.width
#                if border_width > self.y:
#                    self.y = border_width
#
#                if self.y + self.height > s_height - border_width:
#                    self.y = s_height - border_width - self.height



        def draw(self): #Tegner markeringsfirkanten
            #pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
            if self.selected:
                pygame.draw.rect(win, (255,255,255), (self.x, self.y, self.width,self.height), 2) #Tegner omrissen til knappen

    def button_click(): #Styrer lengden på klikket | Kontrollerer at knappens handling ikke varer evig
        for button in buttons:
            if button.types == "click":
                button.bool = False


    def redraw(): #Tegner alle knappene
        win.fill((0,0,0)) #Fyller bakgrunnen med svart
        global string
        global musics
        global controls
        if not options:
            images_buttons = [pygame.image.load("ButtonPlay.png"), pygame.image.load("ButtonOptions.png"), pygame.image.load("ButtonQuit.png")] #Importerer knappene 
            if started:
                images_buttons[0] = pygame.image.load("ButtonResume.png")
                images_buttons[2] = pygame.image.load("ButtonReturnMM.png")
        else:
            images_buttons = [pygame.image.load("Return.png"), pygame.image.load("ButtonConWD.png"), pygame.image.load("ButtonMusOn.png")]
            if controls == 2:
                images_buttons[1] = pygame.image.load("ButtonConArr.png")
            if musics == False:
                images_buttons[2] = pygame.image.load("ButtonMusOff.png")
            if not started:
                images_buttons.append(pygame.image.load("Difficulty" + game_difficulty + ".png"))
        if len(buttons) != 0:
            for i in buttons:
                win.blit(images_buttons[buttons.index(i)], (i.x, i.y))
        for button in buttons:
            button.draw()

        pygame.display.update() #Oppdaterer skjermen



    def options_screen(): #Lager skjermen for options
        global options
        options = True
        ferdig = False
        buttons.clear()
        run_other = True
        while run_other: 
            clock.tick(fps)
            global mx, my
            mx, my = pygame.mouse.get_pos()
            for button in buttons:
                button.select()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN: #Sjekker om man klikker
                    for button in buttons: #Sjekker dette i alle knappene
                        button.check() 

                if event.type == pygame.QUIT: #Quit-knappen | Avslutter alt
                    run_other = False
                    global play, slutt
                    global run
                    run = False
                    play = False
                    slutt = False
                    global quits
                    quits = True
                # win_color = pygame.Color(Colors[x])
                # win.fill(win_color)
                # pygame.draw.rect(win, (255, 0, 0), (10, 10, 100, 100))
                # pygame.display.update()
#                for button in buttons:
#                    if button.types == "move" and button.bool:
#                        if not (border_width > mx or mx > s_width - border_width or border_width > my or my > s_height - border_width):
#                            button.move()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]: #Lukker optionsscreen
                run_other = False
                ferdig = True


            global click_delay #Kontrolerer et delay mellom trykkene
            if click_delay > 0:
                click_delay -= 1

            start = True
            if len(buttons) == 0:
                buttons.append(Button(125, 425, 750, 50, "click", "yellow")) #Legger til knappene
                buttons.append(Button(100, 25, 800, 100, "click", "purple"))
                buttons.append(Button(100, 160, 800, 100, "click", "blue"))
                if not started:
                    buttons.append(Button(100, 295, 800, 100, "click", "blue"))


            if start: #Sjekker alle knappene og utfører handlingen til knappen dersom aktivert
                if buttons[0].bool:
                    run_other = False
                    buttons.clear() #Quit tilbake til Meny
                else:
                    if buttons[1].bool: #controls
                        global controls
                        if controls == 1:
                            controls = 2
                        else:
                            controls = 1
                    if buttons[2].bool:
                        global musics #Musikk
                        if musics:
                            musics = False
                            if started:
                                pygame.mixer.music.stop()
                        else:
                            musics = True
                            if started:
                                pygame.mixer.music.play(-1) #Spiller sangen uendelig
                    if not started:
                        if buttons[3].bool:
                            global game_difficulty #Vanskelighetsgraden til spillet
                            if game_difficulties.index(game_difficulty) != game_difficulties.index(game_difficulties[-1]):
                                game_difficulty = game_difficulties[game_difficulties.index(game_difficulty)+1]
                            else:
                                game_difficulty = game_difficulties[0]


            button_click() 
            if ferdig: #Tømmer knappelisten
                buttons.clear()

            redraw()


    def start_screen(): #Play, Options og Quit skjerm - fungerer likt som optionsfunksjonen. Knappene har andre egenskaper

        buttons.clear()
        global game_inits
        global quits
        run_other = True

        while run_other:
            global options
            options = False
            clock.tick(fps)
            if quits == True:
                run_other = False
                game_inits = False
            else:
                run_other = True
                global mx, my
                mx, my = pygame.mouse.get_pos() #Finner posisjonen til musen
                for button in buttons:
                    button.select()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN: #Sjekker om man klikker
                        for button in buttons:
                            button.check()

                    if event.type == pygame.QUIT:
                        run_other = False
                        global run
                        run = False
                        global play, slutt
                        play = False
                        slutt = False
                    # win_color = pygame.Color(Colors[x])
                    # win.fill(win_color)
                    # pygame.draw.rect(win, (255, 0, 0), (10, 10, 100, 100))
                    # pygame.display.update()
                    else:
                        for button in buttons:
                            if button.types == "move" and button.bool:
                                if not (border_width > mx or mx > s_width - border_width or border_width > my or my > s_height - border_width):
                                    button.move()
                                else:
                                    pass
                        global click_delay
                        if click_delay > 0:
                            click_delay -= 1
                        start = True
                        if len(buttons) == 0:
                            buttons.append(Button(100, 25, 800, 100, "click", "purple"))
                            buttons.append(Button(100, 200, 800, 100, "click", "blue"))
                            buttons.append(Button(100, 375, 800, 100, "click", "yellow"))

                        if start:
                            if buttons[0].bool:
                                if quits != True: #Stopper spillet
                                    game_inits = True
                                run_other = False

                            elif buttons[1].bool:
                                options_screen() #Options

                            elif buttons[2].bool:
                                run = False #Starter selve spillet
                                run_other = False
                                if started == False:
                                    play = False
                                global restart
                                restart = True

                        button_click()
                        redraw()
    def debug(): #Renser skjermen
        specials.clear()
        fireballs.clear()
    
    Colors = ["purple", "black", "yellow", "blue", "white", "gray"]
    border_width = 0
    #b = Button(100, 100, 200, 200, "move", "purple")
    buttons = [] #Tom liste for knappene
    #buttons.append(b)
    started = False
    restart = False
    fps = 120
    click_delay = 0
    quits = False
    musics = True
    game_inits = False
    controls = 1
    string = "Play"
    game_difficulty = "Easy" #Starter spillet alltid i Easy-mode
    game_difficulties = ["Cheats", "Easy", "Medium", "Hard"] #Vanskelighetsgradene
    
    room_2 = True
    room_3 = True
    room_4 = True
    room_5 = True
    room_6 = True
    room_7 = True
    room_8 = True
    room_9 = True

    start_screen()
    if game_inits: 
        minimaps = False
        minimap = False
        rooms = []
        cords = []
        quitt = False
        pluss = 1 #Ekstrapoeng for å drepe bossen
        boss_delay_attack = 0
        minimap_delay = 0
        lost = True
        if game_difficulty == "Cheats": #Styrer vanskelighetskravet - mindre damage per vanskelighetsgrad
            damage = 9
        elif game_difficulty == "Easy":
            damage = 9
        elif game_difficulty == "Medium":
            damage = 6
        else:
            damage = 3
        Bosses = False
        started = True
        string = "Resume"
        buttons.clear()

### Alle verdiene til borderene, brukes ikke men inneholder informasjonen til borderene
#        border_ul = platform(0, 0, s_width / 2 - 50, 25)
#        border_ur = platform(s_width / 2 + 50, 0, s_width / 2 - 50, 25)
#        border_u = platform(0, 0, s_width, 25)
#        border_ru = platform(s_width - 25, 0, 25, s_height / 2 - 50)
#        border_rd = platform(s_width - 25, s_height / 2 + 50, 25, s_height / 2 - 50)
#        border_r = platform(s_width - 25, 0, 25, s_height)
#        border_dl = platform(0, s_height - 25, s_width / 2 - 50, 25)
#        border_dr = platform(s_width / 2 + 50, s_height - 25, s_width / 2 - 50, 25)
#        border_d = platform(0, s_height - 25, s_width, 25)
#        border_lu = platform(0, 0, 25, s_height / 2 - 50)
#        border_ld = platform(0, s_height / 2 + 50, 25, s_height / 2 - 50)
#        border_l = platform(0, 0, 25, s_height)

        song_change = True #Styrer sangbytte
        song_replay = True
        show = True
        kniver = [] #Tom liste for knivene
        man.delay = 0 #Delay for spiller, kniv, enemies osv.
        knife.delay = 0
        enemy_delay = 0
        time_delay = 0
        time = 0
        bakShow = True
        run = True
        kastespeed = 27
        slutt = True
        music = pygame.mixer.music.load(songs[0]) #Musikk som spilles
        Boss_fight = True
        respawn_delay = 0
        man_hit_delay = 0
        font = pygame.font.SysFont('comicsans', 30, True)
        while run and man.health > 0:  # Hovedloop
            if boss_delay_attack > 0:
                boss_delay_attack -= 1
            dont_draw = False
            if man_hit_delay != 0:
                if man_hit_delay in [4,5,6,7,1,10,11,12,13,16,17,18,19,22,23,24,25]:
                    dont_draw = True
                man_hit_delay -= 1
            if room == 10 and song_replay: #Sjekker opp om rommet er 10 og om den har byttet sang
                song_change = True
                if Bosses == False and Boss_fight == True: #Starter bossfighten
                    Main_Boss = Boss(450, 200, 100, 100, 600) #Definerer bossen
                    spawnx = [] #Styrer spawnet til enemies
                    spawny = []
                    for x in range(200, 401 - 40):
                        spawny.append(x)
                    for x in range(450, 551 - 50):
                        spawnx.append(x)
                    Bosses = True
                    enemies.append(Main_Boss)
                    Boss_projectiles_width = 5 #Informasjon for projektilene
                    Boss_projectiles_radius = 5
                    Main_Boss.atkpattern = 1

                    projectile_radius = 5

                    hjørne_koordinater = {"N": ["TBL", "TL", "TTL", "TTR", "TR", "TBR"], #Ordliste for plasseringerav spiller 
                                          "S": ["BTL", "BL", "BBL", "BBR", "BR", "BTR"],
                                          "E": ["TTR", "TR", "TBR", "BTR", "BR", "BBR"],
                                          "W": ["TTL", "TL", "TBL", "BTL", "BL", "BBL"]}
                    
                    #Ordliste for bevegelsen til projektilene
                    koordinater = {"N": (Main_Boss.x + Main_Boss.width * (1 / 10), Main_Boss.y - Boss_projectiles_width, 
                                         Main_Boss.width * (8 / 10), Boss_projectiles_width),
                                   "S": (Main_Boss.x + Main_Boss.width * (1 / 10), Main_Boss.y + Main_Boss.height,
                                         Main_Boss.width * (8 / 10), Boss_projectiles_width),
                                   "W": (Main_Boss.x - Boss_projectiles_width, Main_Boss.y + Main_Boss.height * (1 / 10),
                                         Boss_projectiles_width, Main_Boss.height * (8 / 10)),
                                   "E": (Main_Boss.x + Main_Boss.width, Main_Boss.y + Main_Boss.height * (1 / 10),
                                         Boss_projectiles_width, Main_Boss.height * (8 / 10)),
                                   "TR": (Main_Boss.x + Main_Boss.width - 15, Main_Boss.y,
                                          Main_Boss.width * (1 / 10) + Boss_projectiles_width,
                                          Main_Boss.height * (1 / 10) + Boss_projectiles_width),
                                   "TL": (Main_Boss.x, Main_Boss.y, Main_Boss.width * (1 / 10) + Boss_projectiles_width,
                                          Main_Boss.height * (1 / 10) + Boss_projectiles_width),
                                   "BR": (Main_Boss.x + Main_Boss.width - 15, Main_Boss.y + Main_Boss.height - 15,
                                          Main_Boss.width * (1 / 10) + Boss_projectiles_width,
                                          Main_Boss.height * (1 / 10) + Boss_projectiles_width),
                                   "BL": (Main_Boss.x, Main_Boss.y + Main_Boss.height - 15,
                                          Main_Boss.width * (1 / 10) + Boss_projectiles_width,
                                          Main_Boss.height * (1 / 10) + Boss_projectiles_width),
                                   "TTR": (Main_Boss.x + Main_Boss.width * (9 / 10) + Boss_projectiles_width,
                                           Main_Boss.y - (Boss_projectiles_width + Boss_projectiles_radius)),
                                   "TBR": (
                                   Main_Boss.x + Main_Boss.width + (Boss_projectiles_width + Boss_projectiles_radius),
                                   Main_Boss.y + Main_Boss.height * (1 / 10) - Boss_projectiles_width),
                                   "TTL": (Main_Boss.x + Main_Boss.width * (1 / 10) - Boss_projectiles_width,
                                           Main_Boss.y - (Boss_projectiles_width + Boss_projectiles_radius)),
                                   "TBL": (Main_Boss.x - (Boss_projectiles_width + Boss_projectiles_radius),
                                           Main_Boss.y + Main_Boss.height * (1 / 10) - Boss_projectiles_width),
                                   "BTR": (
                                   Main_Boss.x + Main_Boss.width + (Boss_projectiles_width + Boss_projectiles_radius),
                                   Main_Boss.y + Main_Boss.height * (9 / 10) + Boss_projectiles_width),
                                   "BBR": (Main_Boss.x + Main_Boss.width * (9 / 10) + Boss_projectiles_width,
                                           Main_Boss.y + Main_Boss.height + (
                                                       Boss_projectiles_width + Boss_projectiles_radius)),
                                   "BTL": (Main_Boss.x - (Boss_projectiles_width + Boss_projectiles_radius),
                                           Main_Boss.y + Main_Boss.height * (9 / 10) + Boss_projectiles_width),
                                   "BBL": (Main_Boss.x + Main_Boss.width * (1 / 10) - Boss_projectiles_width,
                                           Main_Boss.y + Main_Boss.height + (
                                                       Boss_projectiles_width + Boss_projectiles_radius))}
                    x_zone = (s_end_x - s_start_x - Main_Boss.width) / 10
                    y_zone = (s_end_y - s_start_y - Main_Boss.height) / 10


            if Bosses:
                if delay > 0:
                    delay -= 1
                    if delay == 0 and Main_Boss.health <= 400: #Styrer delayet til bossen og spawn til enemies
                        respawn_delay += 1


                else:
                    if Main_Boss.atkpattern == 1: #Endrer angrepsmønster
                        Main_Boss.atkpattern = 2
                        boss_delay_attack = 27
                    else:
                        Main_Boss.atkpattern = 1
                        boss_delay_attack = 27
                    delay = 54
                if respawn_delay == 3: #Styrer spawn til enemies på boss level
                    telle = True
                    enemy_create(2)
                    respawn_delay = 0
                if delay % 3 == 0:
                    Main_Boss.search()

                for projectile in projectiles: #Beveger projektilene
                    projectile.move()
                    projectile.hit()

            if song_change: #Endrer sangen dersom man når bossrommet
                if room == 1:
                    if musics == True:
                        pygame.mixer.music.play(-1)
                        song_change = False
                elif room == 10:
                    music = pygame.mixer.music.load(songs[1])
                    if musics == True:
                        pygame.mixer.music.play(-1)
                    song_change = False
                    song_replay = False

            #    print(round(clock.get_fps(),0))

            if time_delay % 27 == 0:
                time += 1

            if knife.delay > 0: #Delay for knivkastingen
                knife.delay -= 1

            if len(enemies) == 0:
                if room == 1 and not (key1.open): #Viser nøklene 
                    key1.show = True
                if room == 2 and not (key2.open):
                    key2.show = True
                if room == 3 and not (key3.open):
                    key3.show = True
                if room == 4 and not (key4.open):
                    key4.show = True
                if room == 5 and not (key5.open):
                    key5.show = True
                if room == 6 and not (key6.open):
                    key6.show = True
                if room == 7 and not (key7.open):
                    key7.show = True
                if room == 8 and not (key8.open):
                    key8.show = True
                if room == 9 and not (key9.open):
                    key9.show = True
            else:
                if room == 1: 
                    key1.show = False #Gjemmer nøklene
                if room == 2:
                    key2.show = False
                if room == 3:
                    key3.show = False
                if room == 4:
                    key4.show = False
                if room == 5:
                    key5.show = False
                if room == 6:
                    key6.show = False
                if room == 7:
                    key7.show = False
                if room == 8:
                    key8.show = False
                if room == 9:
                    key9.show = False

            clock.tick(27)
            if man.delay > 0: #Styrer en intern timer for man og enemy
                man.delay -= 1
            if enemy_delay > 0:
                enemy_delay -= 9
            else:
                enemy_delay = 27

            time_delay += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT: #Stopper skriptet helt
                    run = False
                    play = False
                    slutt = False
                    quitt = True
            if special_delay > 0:
                special_delay -= 1
           
            keys = pygame.key.get_pressed() #Definerer alle knappene på tastaturet
            
            if keys[pygame.K_TAB]: #Dersom man klikker TAB vis Minimap
                minimap = True
            else:
                minimap = False
                
                #Kaster Kniver dersom man klikker SPACE
                if keys[pygame.K_SPACE] and knife.delay == 0:  # antall projektiler som kan være på skjermen
                    kniver.append(knife())
                    knife.delay = kastespeed
                for kniv in kniver:
                    kniv.move()

                if room == 1: #Definerer bakgrunnen til det den skal være basert på rommet
                    bg = pygame.image.load("BakRoom1.png")
                    bak = False
                elif room == 2:
                    bg = pygame.image.load("BakRoom2.png")
                elif room == 3:
                    bg = pygame.image.load("BakRoom3.png")
                elif room == 4 or room == 5 or room == 7 or room == 8:
                    bg = pygame.image.load("BakRoom5.png")
                elif room == 6:
                    bg = pygame.image.load("BakRoom6.png")
                elif room == 9:
                    bg = pygame.image.load("BakRoom9.png")
                else:
                    bg = pygame.image.load("BakRoom10.png")

                if room == 1 and bakShow == True and man.x + man.width < 550 and man.x + man.width > 450:
                    if man.y + man.height > 200 and man.y + man.height < 300:
                        bg = pygame.image.load("BakRoom1_Info.png") #Dersom man er innenfor dette område så vises info og stopper alt annet
                        bak = True
                        show = False #Når man har gått ut kan man ikke gå inn igjen
                else:
                    bakShow = False

                for fiende in enemies:
                    if bak == True:
                        fiende.vel = 0 #Stopper enemies dersom infosiden er åpen
                    else:
                        fiende.vel = 3

                #Powerups
                if gethe == True and kiste1.open == True and man.health < 4 and len(enemies) == 0:
                    man.health += 1 #Gir et ekstra liv 
                    gethe = False

                if getpo == True and kiste2.open == True and len(enemies) == 0:
                    kastespeed = 14 #Øker kastehastigheten
                    getpo = False

                if getda == True and kiste3.open == True and len(enemies) == 0:
                    damage *= 2 #Øker skaden en gjør
                    getda = False

                if keys[pygame.K_q] and special_delay == 0: #Dersom man klikker L bruker man special angrep
                    man.special()

                for spec in specials: #Bevegelse for spesial angrepet 
                    spec.move()
                for firebal in fireballs:
                    firebal.move()
                    firebal.special()

                if len(enemies) == 0: #Kiste animasjon | Dersom det ikke er noen enemies
                    if man.x < kiste1.x + kiste1.width and man.x + man.width > kiste1.x and room == 3: #Room 3 og kollisjon
                        if man.y + man.height > kiste1.y and man.y < kiste1.y + kiste1.height:
                            kiste1.open = True #Åpne kiste 1

                    if man.x < kiste2.x + kiste2.width and man.x + man.width > kiste2.x and room == 6:
                        if man.y + man.height > kiste2.y and man.y < kiste2.y + kiste2.height:
                            kiste2.open = True #Åpne kiste 2

                    if man.x < kiste3.x + kiste3.width and man.x + man.width > kiste3.x and room == 9:
                        if man.y + man.height > kiste3.y and man.y < kiste3.y + kiste3.height:
                            kiste3.open = True #Åpne kiste 3

                    # Skjekker om spiller treffer nøkkel | Skjuler den da og åpner døren
                    if man.x < key1.x + key1.width and man.x + man.width > key1.x and room == 1:
                        if man.y + man.height > key1.y and man.y < key1.y + key1.height:
                            key1.show = False
                            key1.open = True

                    if man.x < key2.x + key2.width and man.x + man.width > key2.x and room == 2:
                        if man.y + man.height > key2.y and man.y < key2.y + key2.height:
                            key2.show = False
                            key2.open = True

                    if man.x < key3.x + key3.width and man.x + man.width > key3.x and room == 3:
                        if man.y + man.height > key3.y and man.y < key3.y + key3.height:
                            key3.show = False
                            key3.open = True

                    if man.x < key4.x + key4.width and man.x + man.width > key4.x and room == 4:
                        if man.y + man.height > key4.y and man.y < key4.y + key4.height:
                            key4.show = False
                            key4.open = True

                    if man.x < key5.x + key5.width and man.x + man.width > key5.x and room == 5:
                        if man.y + man.height > key5.y and man.y < key5.y + key5.height:
                            key5.show = False
                            key5.open = True

                    if man.x < key6.x + key6.width and man.x + man.width > key6.x and room == 6:
                        if man.y + man.height > key6.y and man.y < key6.y + key6.height:
                            key6.show = False
                            key6.open = True
                    if man.x < key7.x + key7.width and man.x + man.width > key7.x and room == 7:
                        if man.y + man.height > key7.y and man.y < key7.y + key7.height:
                            key7.show = False
                            key7.open = True

                    if man.x < key8.x + key8.width and man.x + man.width > key8.x and room == 8:
                        if man.y + man.height > key8.y and man.y < key8.y + key8.height:
                            key8.show = False
                            key8.open = True
                    if man.x < key9.x + key6.width and man.x + man.width > key9.x and room == 9:
                        if man.y + man.height > key9.y and man.y < key9.y + key9.height:
                            key9.show = False
                            key9.open = True
                
            # Skjekker om spiller treffer dør
                # Skjekker opp og ned
                if man.x > s_width / 2 - man.width - 23 and man.x + man.width < s_width / 2 + man.width + 20:
                    if man.y < man.vel + 1:
                        if keys[pygame.K_f] and key1.open and room == 1:

                            door1.locked = False

                        elif not (door1.locked) and room == 1: #Styrer overgangen mellom rom
                            man.y = s_height - man.height - 20
                            room = 2
                            debug()
                            if room_2:
                                telle = True #Lar enemies spawne
                                room_2 = False

                        elif keys[pygame.K_f] and key2.open and room == 2:
                            door2.locked = False

                            antall = 3 #antall enemies i rom 2

                        elif not (door2.locked) and room == 2: #Overgang
                            win_color = (200, 128, 24)
                            man.y = s_height - man.height - 20
                            room = 3
                            debug()
                            if room_3:
                                telle = True
                                room_3 = False

                    if man.y > s_height - man.vel - 1 - man.height: #Overgang tilbake
                        if room == 2 and key2.open:
                            man.y = 20
                            room = 1
                            debug()

                        elif room == 3 and key3.open: 
                            man.y = 20
                            room = 2
                            debug()

                        elif keys[pygame.K_f] and key9.open and room == 1:
                            door9.locked = False

                            antall = 1

                        elif not (door9.locked) and room == 1:
                            man.y = 20
                            room = 10
                            debug()

                # Skjekker til siden
                if man.y > s_height / 2 - man.height - 23 and man.y + man.height < s_height / 2 + man.width + 20:

                    if man.x > s_width - man.vel - man.width - 1:
                        # Høyre siden fremover

                        if keys[pygame.K_f] and key3.open and room == 2:
                            door3.locked = False

                            antall = 2 #Spawn antall

                        elif not (door3.locked) and room == 2: #Overgang
                            man.x = 20
                            room = 4
                            debug()
                            if room_4:
                                telle = True
                                room_4 = False

                        elif keys[pygame.K_f] and key4.open and room == 4:
                            door4.locked = False

                            antall = 3 #Spawn antall

                        elif not (door4.locked) and room == 4: #Overgang
                            man.x = 20
                            room = 5
                            debug()
                            if room_5:
                                telle = True
                                room_5 = False

                        elif keys[pygame.K_f] and key5.open and room == 5: #Spawn antall
                            door5.locked = False

                            antall = 3

                        elif not (door5.locked) and room == 5: #Overgang
                            man.x = 20
                            room = 6
                            debug()
                            if room_6:
                                telle = True
                                room_6 = False

                        # Venstre siden bakover
                        if room == 7 and key7.open: #Gå tilbake gjennom døren
                            man.x = man.width + 20
                            room = 2
                            debug()

                        elif room == 8 and key8.open:
                            man.x = man.width + 20
                            room = 7
                            debug()

                        elif room == 9 and key9.open:
                            man.x = man.width + 20
                            room = 8
                            debug()

                    if man.x < man.vel:
                        # Høyre siden bakover

                        if room == 6 and key6.open:
                            man.x = s_width - man.width - 20
                            room = 5
                            debug()

                        elif room == 5 and key5.open:
                            man.x = s_width - man.width - 20
                            room = 4
                            debug()

                        elif room == 4 and key4.open:
                            man.x = s_width - man.width - 20
                            room = 2
                            debug()

                        # Venstre siden fremover
                        elif keys[pygame.K_f] and key6.open and room == 2: #Spawn antall
                            door6.locked = False

                            antall = 3

                        elif not (door6.locked) and room == 2: #Overgang
                            man.x = s_width - man.width - 20
                            room = 7
                            debug()
                            if room_7:
                                telle = True
                                room_7 = False

                        elif keys[pygame.K_f] and key7.open and room == 7: #Spawn
                            door7.locked = False

                            antall = 3

                        elif not (door7.locked) and room == 7: #Overgang
                            man.x = s_width - man.width - 20
                            room = 8
                            debug()
                            if room_8:
                                telle = True
                                room_8 = False

                        elif keys[pygame.K_f] and key8.open and room == 8: #Spawn
                            door8.locked = False
                            antall = 3

                        elif not (door8.locked) and room == 8: #Overgang
                            man.x = s_width - man.width - 20
                            room = 9
                            debug()
                            if room_9:
                                telle = True
                                room_9 = False

                # Bevegelse for spiller
                if controls == 2: #Om man endrer kontrollene i settings | Piltaster
                    if keys[pygame.K_RIGHT]:
                        if man.x < s_width - man.width - man.vel:
                            man.x += man.vel #Hastighet
                            man.left = 0 #Retninger
                            man.right = 1
                            man.up = 0
                            man.down = 0
                            man.standing = False #Styrer om man beveger seg
                            man.retning = 2 #Retning
                        else:
                            man.x = s_width - man.width

                    elif keys[pygame.K_LEFT]: #Venstre | Likt som over
                        if man.x > man.vel:
                            man.x -= man.vel
                            man.left = 1
                            man.right = 0
                            man.down = 0
                            man.up = 0
                            man.standing = False
                            man.retning = 1
                        else:
                            man.x = 0

                    elif keys[pygame.K_UP]: #Opp
                        if man.y > man.vel:
                            man.y -= man.vel
                            man.left = 0
                            man.right = 0
                            man.down = 0
                            man.up = 1
                            man.standing = False
                            man.retning = 4
                        else:
                            man.y = 0

                    elif keys[pygame.K_DOWN]: #Ned
                        if man.y < s_height - man.height - man.vel:
                            man.y += man.vel
                            man.left = 0
                            man.right = 0
                            man.down = 1
                            man.up = 0
                            man.standing = False
                            man.retning = 3

                        else:
                            man.y = s_height - man.height
                    else:
                        man.standing = True
                        man.walkCount = 0

                else: #WASD
                    if keys[pygame.K_d]: #Høyre
                        if man.x < s_width - man.width - man.vel:
                            man.x += man.vel
                            man.left = 0
                            man.right = 1
                            man.up = 0
                            man.down = 0
                            man.standing = False
                            man.retning = 2
                        else:
                            man.x = s_width - man.width

                    elif keys[pygame.K_a]: #Venstre
                        if man.x > man.vel:
                            man.x -= man.vel
                            man.left = 1
                            man.right = 0
                            man.down = 0
                            man.up = 0
                            man.standing = False
                            man.retning = 1
                        else:
                            man.x = 0

                    elif keys[pygame.K_w]: #Opp
                        if man.y > man.vel:
                            man.y -= man.vel
                            man.left = 0
                            man.right = 0
                            man.down = 0
                            man.up = 1
                            man.standing = False
                            man.retning = 4
                        else:
                            man.y = 0

                    elif keys[pygame.K_s]: #Ned
                        if man.y < s_height - man.height - man.vel:
                            man.y += man.vel
                            man.left = 0
                            man.right = 0
                            man.down = 1
                            man.up = 0
                            man.standing = False
                            man.retning = 3

                        else:
                            man.y = s_height - man.height
                    else:
                        man.standing = True
                        man.walkCount = 0
               
                if keys[pygame.K_ESCAPE]: #Åpner pause dersom man klikker escape
                    start_screen()
                if keys[pygame.K_u] and game_difficulty == "Cheats": #Bruk U for å "Slette" enemies i cheats
                    for fiende in enemies:
                        fiende.health -= damage

            for fiende in enemies: #Sjekker kollisjon mellom kniv og fiende
                for kniv in kniver:
                    if kniv.x < fiende.x + fiende.width and kniv.x + kniv.width > fiende.x:
                        if kniv.y + kniv.height > fiende.y and kniv.y < fiende.y + fiende.height:
                            fiende.health -= damage 
                            kniver.pop(kniver.index(kniv))

                if man.x < fiende.x + fiende.width and man.x + man.width > fiende.x: #Sjekker kollisjon mellom spiller og fiende
                    if man.y + man.height > fiende.y and man.y < fiende.y + fiende.height:
                        if man_hit_delay == 0:

                            if man_hit_delay == 0: #Sskaper et delay mellom skadene
                                man.hit()
                                man.health -= 1
                                man_hit_delay = 27

            man.hit()

            for fiende in enemies: #Bevegelse for enemies
                fiende.move()

            if man.health == 0: #Stopper spillet dersom du dør og sender spiller til Game Over
                    enemies.clear()
                    run = False

            if Bosses:
                if Main_Boss.health < 1:
                        pluss = 10
                else:
                    pluss = 1
            if Bosses:
                if Main_Boss.health <= 0: #Avslutter programmet dersom bossen mister all hp-en
                    lost = False 
                    run = False
                    Bosses = False
                    Boss_fight = False
                else:
                    lost = True
            if not minimap: #Tegner skjermen dersom minimapet ikke vises
                redrawGamewindow()
            else:
                redraw_minimap() #Tegner minimapet
    credit = False            
    def draw_window(): #Tegner den siste skjermene (Game Over og Credits)
        global bg
        global win
        win.blit(bg, (0,0)) #gir bakgrunnen bildet bg (variabel)
        for button in buttons:
            win.blit(pygame.image.load("ButtonCredits.png"), (button.x, button.y)) #Tegner Credits-knappen
            button.draw() #Tegner knappene
        if credit == False:
            text = font.render("Your score is: " + str(formel), 1, (0,0,0)) #Printer skåren din til skjermen 
            win.blit(text, (400, 225))
        pygame.display.update()
    if restart == False or play == False:
        if game_inits:

            if slutt: #Endrer bakgrunnen og tar bort knappene
                endre_bg = True
            buttons.clear()
            but = False
            while slutt:
                global formel
                formel = ((drepte_enemies * pluss) * man.health)*game_difficulties.index(game_difficulty) #Formel for poengene
                if endre_bg:
                    if lost == False:
                        bg = pygame.image.load('Win.png') #Viser Win-skjerm dersom du vant
                        
                    else:
                        bg = pygame.image.load('GameOver.png') #Viser Game Over dersom du tapte

                    endre_bg = False

                if but == False:
                    buttons.append(Button(100, 375, 800, 100, "click", "purple"))
                dont_draw = True
                man.standing = True #Sjekker om spiller står stille
                man.x = 0 #Koordinatene til spiller ved slutt
                man.y = 0
                global mx, my
                mx, my = pygame.mouse.get_pos()
                for button in buttons:
                    button.select()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN: #Sjekker om man klikker
                        for button in buttons:
                            button.check()
                    if event.type == pygame.QUIT: #Avslutter spillet og vinduet
                        slutt = False
                        play = False


                if click_delay > 0:
                    click_delay -= 1
                if but == False:
                    if buttons[0].bool:
                        bg = pygame.image.load("Credits.png") #Tegner Credits og deretter skjuler den 
                        credit = True
                        buttons.clear()
                        but = True

                button_click()
                draw_window()
    pygame.quit() #Slutter pygame og avslutter spillet helt