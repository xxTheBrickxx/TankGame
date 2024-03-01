import pygame
import math
import helper as hlp

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
                                              hlp.radtodegrees(self.angle) - 90)

  def draw(self, surface, tanklist):

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
      b.draw(surface, tanklist)

  def drawhitbox(self, surface):

    tank_rect = self.currentimg.get_rect(center=(self.x, self.y + 13))
    pygame.draw.rect(surface, pygame.Color(255, 0, 0), tank_rect)
  def takeinput(self):
    for event in pygame.event.get:
      if event.type == pygame.KEYDOWN:
  
        if event.key == ord("w"):
          self.moveforward = 1
        if event.key == ord("a"):
          self.turnleft = -1
        if event.key == ord("s"):
          self.movebackward = -1
        if event.key == ord("d"):
          self.turnright = 1
        if event.key == pygame.K_LSHIFT:
          if self.alive:
            bullet1 = Bullet(hlp.bulletstartoffsetx(self.x, self.angle),
                             hlp.bulletstartoffsety(self.y, self.angle) + 13, 10,self.angle, self)
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
      self.angle += hlp.degreestorad(1) * self.speed

    if self.turn == 1:
      self.angle -= hlp.degreestorad(1) * self.speed

class Bullet:

  def __init__(self, x, y, speed, angle, owner):
    self.x = x
    self.y = y
    self.speed = owner.bulletspeed
    self.damage = 0
    self.angle = angle
    self.owner = owner
    self.originalimg = pygame.image.load("tank bulet.png")
    self.currentimg = pygame.transform.scale(self.originalimg, (35 / 6, 13 / 6))
    self.imgsteptwo = pygame.transform.rotate(self.currentimg, hlp.radtodegrees(self.angle))

  def draw(self, surface, tanklist):
    self.x += math.cos(self.angle) * self.speed
    self.y += math.sin(self.angle) * -self.speed
    if self.speed != 0:
      surface.blit(self.imgsteptwo, (self.x, self.y))
      self.bullethitcheck(tanklist)

  def bullethitcheck(self, tanklist):
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