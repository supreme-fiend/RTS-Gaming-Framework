# Generic RTS game with 2 races having different types of combat units


import pygame
import numpy as np
import os

pygame.init()

win = pygame.display.set_mode((1000, 700))

pygame.display.set_caption("Generic RTS Game")

players = []

def refresh():
    win.fill((0,0,0))
    for player in players:
        for unit in player.units:
            if (unit.health <= 0):
                player.units.remove(unit)
            unit.move()
            unit.draw()

        for struct in player.structures:
            struct.draw()

        for projectile in player.projectiles:
            projectile.draw()
            projectile.move()
    pygame.display.update()

def deselect_all():
    for player in players:
        for unit in player.units:
            unit.selected = False

class Projectile:
    def __init__(self, ap, x, y, x2, y2, v, p_i):
        self.attack = ap
        self.x = x
        self.y = y
        self.speed = v
        self.targetx = x2
        self.targety = y2
        players[p_i].projectiles.append(self)
        
    def move(self):
        if (self.targetx != self.x and self.targety != self.y):
            distance = np.sqrt ((self.tagetx - self.x)**2 + (self.targety - self.y)**2)
            time = distance/self.speed
            Vx = (self.targetx - self.x)/time
            Vy = (self.targety - self.y)/time
            if (np.abs(self.targetx - self.x) >= 2 or np.abs(self.targety - self.y) >= 2):
                self.x += Vx
                self.y += Vy
            else:
                self.targetx = self.x
                self.targety = self.y



class Unit:
    def __init__(self, hp, ap, dp, sp, x, y, t, p_i):
        self.health = hp
        self.attack = ap
        self.defense = dp
        self.speed = sp

        self.x = x
        self.y = y
        self.movetox = x
        self.movetoy = y
        self.type = t
        self.p_i = p_i
        imgpath = t + ".png"
        imgpath = os.path.join(os.getcwd(), imgpath)

        #NOTE : ALL UNIT IMAGES MUST BE 50x50 PIXELS!!
        self.image = pygame.image.load(imgpath)
        self.carry = []
        self.selected = False
        players[p_i].units.append(self)

    def draw(self):
        if self.selected:
            pygame.draw.rect(win, (0,0,255), (self.x-5, self.y-5, 60, 60))
        win.blit(self.image, (self.x, self.y))
        pygame.draw.rect(win, (0,255,0), (self.x, self.y, 2, self.health/10))

    def move(self):
        if self.movetox != self.x and self.movetoy != self.y:    
            distance = np.sqrt ((self.movetox - self.x)**2 + (self.movetoy - self.y)**2)
            time = distance/self.speed
            Vx = (self.movetox - self.x)/time
            Vy = (self.movetoy - self.y)/time
            if (np.abs(self.movetox - self.x) >= 2 or np.abs(self.movetoy - self.y) >= 2):
                self.x += Vx
                self.y += Vy
            else:
                self.movetox = self.x
                self.movetoy = self.y

    def attack(self, target):
        b = Projectile(self.attack, self.x + 60, self.y + 60, 2, self.p_i)

    
    def is_over(self, mouse_pos):
        if (mouse_pos[0] >= self.x and mouse_pos[0] <= (self.x + 60)) and (mouse_pos[1] >= self.y and mouse_pos[1] <= self.y + 60):
            return True
        return False


class Structure:
    def __init__(self, t, x, y, p_i):
        self.type = t
        imgpath = t + ".png"
        imgpath = os.path.join(os.getcwd(), imgpath)
        self.x = x
        self.y = y
        self.image = pygame.image.load(imgpath)
        players[p_i].structures.append(self)
    
    def draw(self):
        win.blit(self.image, (self.x, self.y))


class Player:
    def __init__(self, m, r):
        self.money = m
        self.units = []
        self.structures = []
        self.projectiles = []
        self.index = len(players)
        self.race = r
        players.append(self)

    def deselect_all(self):
        for unit in self.units:
            unit.selected = False

    def spawn_unit (self, hp, ap, dp, sp, x, y, t):
        u = Unit(hp, ap, dp, sp, x, y, t, self.index)

    def build_structure(self, t, x, y):
        s = Structure(t, x, y, self.index)

temp = Player (200, "Wuldar")
temp.spawn_unit (200, 20, 10, 1, 500, 350, "Gatherer")

temp1 = Player(700, "Human")
temp1.spawn_unit(300, 40, 20, 0.1, 250, 250, "Marine")
temp1.build_structure("Barracks", 80, 80)


run = True

while run:
    refresh()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            for p1 in players:
                for u1 in p1.units:
                    if u1.selected and u1.is_over(pygame.mouse.get_pos()):
                        u1.selected = False

                    elif u1.selected == False and u1.is_over(pygame.mouse.get_pos()):
                        u1.selected = True

                    elif u1.selected and not(u1.is_over(pygame.mouse.get_pos())):
                        flag = False
                        for p2 in players:
                            for u2 in p2.units:
                                if u2.is_over(pygame.mouse.get_pos()):
                                    flag = True
                                    if p1.race == p2.race:
                                        if (u1 == u2):
                                            u1.selected = False
                                        else:
                                            u1.selected = False
                                            u2.selected = True
                                    else:
                                        #NOTE: CHANGE THIS PART TO MAKE ATTACK HAPPEN
                                        u1.movetox = u2.x
                                        u1.movetoy = u2.y
                                        u1.selected = False
                        if (flag == False):
                            u1.movetox = pygame.mouse.get_pos()[0]
                            u1.movetoy = pygame.mouse.get_pos()[1]
                            u1.selected = False


                            




exit()

