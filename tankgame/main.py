import random
import pygame
import math
import sys
import time


class Tank:

  def __init__(
      self,
      statsdict,
      x,
      y,
      angle,
      id,
  ):
    self.x = x
    self.y = y
    self.speed = statsdict["speed"]
    # angle is in radians
    self.angle = angle
    self.originalimg = pygame.image.load(statsdict["image"]).convert_alpha()
    self.currentimg = self.originalimg
    self.bulletspeed = statsdict["bulletspeed"]
    self.bulletdamage = statsdict["bulletdamage"]
    self.reloadtime = statsdict["reloadtime"]
    self.maxhp = statsdict["hp"]
    self.hp = statsdict["hp"]
    self.id = id
    self.moveforward = 0
    self.movebackward = 0
    self.turnleft = 0
    self.turnright = 0
    self.moveforwardorback = 0
    self.turn = 0
    self.alive = True
    self.bulletlist = []

  def hpbar(self, surface):
    hpremain = self.hp / self.maxhp
    if self.alive:
      hpredbarrect = pygame.draw.rect(
          surface, (128, 0, 0), pygame.Rect(self.x - 28, self.y - 20, 50, 10))
      hpgreenbarrect = pygame.draw.rect(
          surface, (30, 143, 58),
          pygame.Rect(self.x - 28, self.y - 20, hpremain * 50, 10))

  def rotate(self):
    self.currentimg = pygame.transform.rotate(self.originalimg,
                                              radtodegrees(self.angle) - 90)

  def draw(self, surface):

    if self.hp <= 0:
      self.currentimg = pygame.image.load("Crater.png")
      print("crater")
      print(self.id)
      self.alive = False
    surface.blit(self.currentimg,
                 (self.x - int(self.currentimg.get_width() / 2),
                  self.y - int(self.currentimg.get_height() / 2 - 13)))
    self.hpbar(surface)
    for b in self.bulletlist:
      b.draw(WIN)

  def drawhitbox(self, surface):

    tank_rect = self.currentimg.get_rect(center=(self.x, self.y + 13))
    pygame.draw.rect(surface, pygame.Color(255, 0, 0), tank_rect)

  def movetank(self):
    # move body of this into draw, and have a self.moveforwardorback property
    self.moveforwardorback = self.moveforward + self.movebackward
    if self.moveforwardorback == 1:
      self.x += math.cos(self.angle) * self.speed
      self.y += math.sin(self.angle) * self.speed * -1
    if self.moveforwardorback == -1:
      self.x += math.cos(self.angle) * self.speed * -1
      self.y += math.sin(self.angle) * self.speed

  def shoot(self, bullet):
    bullet.damage = self.bulletdamage
    self.bulletlist.append(bullet)

  def tankturn(self):
    self.turn = self.turnleft + self.turnright
    if self.turn == -1:
      self.angle += degreestorad(1) * self.speed

    if self.turn == 1:
      self.angle -= degreestorad(1) * self.speed

def quitfunction(event):
  if event.type == pygame.QUIT:
    pygame.quit()
    sys.exit()
  if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
    pygame.quit()
    sys.exit()
#bullet 35,13
#tank 24,60
class Bullet:

  def __init__(self, x, y, speed, angle, owner):
    self.x = x
    self.y = y
    self.speed = owner.bulletspeed
    self.damage = 0
    self.angle = angle
    self.owner = owner
    self.originalimg = pygame.image.load("tank bulet.png")
    self.currentimg = pygame.transform.scale(self.originalimg,
                                             (35 / 6, 13 / 6))
    self.imgsteptwo = pygame.transform.rotate(self.currentimg,
                                              radtodegrees(self.angle))

  def draw(self, surface):
    self.x += math.cos(self.angle) * self.speed
    self.y += math.sin(self.angle) * -self.speed
    if self.speed != 0:
      surface.blit(self.imgsteptwo, (self.x, self.y))
      if self.speed != 0:
        self.bullethitcheck()

  def bullethitcheck(self):
    bullet_rect = self.imgsteptwo.get_rect(center=(self.x, self.y + 13))
    for tankindex, tank in enumerate(tanklist):
      tank_rect = tank.currentimg.get_rect(center=(tank.x, tank.y))
      if tank_rect.collidepoint(self.x, self.y - 13):
        if tank.id == self.owner.id:
          break
        print("hit" + str(tankindex))
        self.hitmethod(tank)

  def hitmethod(self, tankhit):
    self.speed = 0
    tankhit.hp -= self.owner.bulletdamage
    print(tankhit.hp)

  def drawhitbox(self, surface):
    bullet_rect = self.imgsteptwo.get_rect(center=(self.x, self.y))
    print(bullet_rect)
    pygame.draw.rect(surface, (255, 87, 51), bullet_rect)


def degreestorad(deg):
  return deg * math.pi / 180


def radtodegrees(rad):
  return rad * 180 / math.pi


def bulletstartoffsetx(x, angle):
  x += math.cos(angle) * 13
  return x


def bulletstartoffsety(y, angle):
  y += math.sin(angle) * -13
  return y


def draw_gameover(surface):
  font = pygame.font.Font("DTM-Mono.otf", 28)
  text = font.render("Player 1 Wins", True, (0, 0, 0))
  text_rect = text.get_rect(center=(screen_w / 2, screen_h / 2))
  surface.blit(text, text_rect)


def draw_gameover2(surface):
  font = pygame.font.Font("DTM-Mono.otf", 28)
  text = font.render("Player 2 Wins", True, (0, 0, 0))
  text_rect = text.get_rect(center=(screen_w / 2, screen_h / 2))
  surface.blit(text, text_rect)


def mouse_postition():
  pass


# global variables and application start

pygame.init()
pygame.font.init()
screen_w = 1050
screen_h = 450
WIN = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)
pygame.display.set_caption("Tanks")

clock = pygame.time.Clock()
fps = 60

tanklist = []
ogtank = {
    "image": "ogtank.png",
    "speed": 5,
    "hp": 100,
    "bulletspeed": 10,
    "bulletdamage": 25,
    "reloadtime": 1
}
greenmonstertank = {
  "image" : "greenmonstertank.png",
  "speed" : 10,
  "hp" : 200,
  "bulletspeed" : 20,
  "bulletdamage" : 50,
  "reloadtime" : 2
}
littletank = {
  
}


#self,x,y,speed,angle,img,hp,id,bulletspeed=10,bulletdamage=25,reloadtime=1
def gamestartmenu(surface):
  startscreen = True
  while startscreen:
    WIN.fill(pygame.Color(0, 0, 0))
    font = pygame.font.Font("DTM-Mono.otf", 28)
    text = font.render("Press space to begin", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen_w / 2, screen_h / 2))
    surface.blit(text, text_rect)
    pygame.display.update()
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
          return("done")
      quitfunction(event)

def tankbattle():

  pygame.display.set_caption("Battle")

  turn = 0
  
  tank1 = Tank(ogtank,
               250,
               250,
               degreestorad(0),
               0)
  tank2 = Tank(greenmonstertank,
               750,
               250,
               degreestorad(180),
               1)
  
  tanklist.append(tank1)
  tanklist.append(tank2)

  running = True
  while running:
    clock.tick(fps)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYDOWN:

        if event.key == ord("w"):
          tank1.moveforward = 1
        if event.key == ord("a"):
          tank1.turnleft = -1
        if event.key == ord("s"):
          tank1.movebackward = -1
        if event.key == ord("d"):
          tank1.turnright = 1
        if event.key == pygame.K_LSHIFT:
          if tank1.alive:
            bullet1 = Bullet(bulletstartoffsetx(tank1.x, tank1.angle),
                             bulletstartoffsety(tank1.y, tank1.angle) + 13, 10,
                             tank1.angle, tank1)
            tank1.shoot(bullet1)
        if event.key == pygame.K_UP:
          tank2.moveforward = 1
        if event.key == pygame.K_DOWN:
          tank2.movebackward = -1
        if event.key == pygame.K_LEFT:
          tank2.turnleft = -1
        if event.key == pygame.K_RIGHT:
          tank2.turnright = 1
        if event.key == pygame.K_RSHIFT:
          if tank2.alive:
            bullet2 = Bullet(bulletstartoffsetx(tank2.x, tank2.angle),
                             bulletstartoffsety(tank2.y, tank2.angle) + 13, 10,
                             tank2.angle, tank2)
            tank2.shoot(bullet2)
        if event.key == pygame.K_ESCAPE:
          pygame.quit()
          sys.exit()

      if event.type == pygame.KEYUP:
        if event.key == ord("a"):
          tank1.turnleft = 0
        if event.key == ord("d"):
          tank1.turnright = 0
        if event.key == ord("w"):
          tank1.moveforward = 0
        if event.key == ord("s"):
          tank1.movebackward = 0
        if event.key == pygame.K_UP:
          tank2.moveforward = 0
        if event.key == pygame.K_DOWN:
          tank2.movebackward = 0
        if event.key == pygame.K_LEFT:
          tank2.turnleft = 0
        if event.key == pygame.K_RIGHT:
          tank2.turnright = 0

    if turn == 1:
      tank1.angle += degreestorad(1)
    if turn == 2:
      tank1.angle -= degreestorad(1)

    WIN.fill(pygame.Color("#ECD796"))

    if tank1.alive:
      tank1.movetank()
      tank1.rotate()
      tank1.tankturn()

    if tank2.alive:
      tank2.movetank()
      tank2.rotate()
      tank2.tankturn()

    if not tank1.alive:
      for b in tank1.bulletlist:
        b.speed = 0
      draw_gameover2(WIN)
      running = False
    if not tank2.alive:
      for b in tank2.bulletlist:
        b.speed = 0
      draw_gameover(WIN)
      running = False

    tank1.draw(WIN)
    tank2.draw(WIN)
    pygame.display.update()

  while True:
    print("done")
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          tanklist.clear()
          return("done")
        quitfunction(event)

    Prespacefont = pygame.font.Font("DTM-Mono.otf", 14)
    prespace = Prespacefont.render("Press space to continue", True,
                                   (161, 153, 153))
    prespacetext_rect = prespace.get_rect(center=(screen_w / 2,
                                                  screen_h / 2 + 50))
    WIN.blit(prespace, prespacetext_rect)
    pygame.display.update()



while True:
  gamestartmenu(WIN)
  print(tankbattle())
pygame.quit()
sys.exit()

# _ tank stats dictionary
# _ menu screen functionality

# example dictionary
# tankstats = { "hp" : 100, "damage" : 10, "image" : image_file}
