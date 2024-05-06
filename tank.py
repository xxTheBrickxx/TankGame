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
      tanklist,
      mineralslist
  ):
    self.x = x
    self.y = y
    self.angle = angle
    self.lastx = x
    self.lasty = y
    self.lastangle = angle
    self.speed = statsdict["speed"]
    self.mineralslist = mineralslist
    # angle is in radians
    self.shadow = pygame.image.load(statsdict["shadow"]).convert_alpha()
    self.shadowpic = None
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
    self.rtime = statsdict["reloadtime"] * 60
    self.shootpossibility = True
    self.reloadpercent = 1
    self.shootsfx = pygame.mixer.Sound("Tankshootsfx.mp3")
    self.tanklist = tanklist
    
    self.deadsfx = pygame.mixer.Sound("Tankdiesfx.wav")
    self.lastturndirection = self.turn
    self.mask = pygame.mask.from_surface(self.currentimg)
    self.maskimage = self.mask.to_surface()
  def hpbar(self, surface):
    hpremain = self.hp / self.maxhp
    if self.alive:
      pygame.draw.rect(
          surface, (128, 0, 0), pygame.Rect(self.x - 28, self.y - 20, 50, 10))
      pygame.draw.rect(
          surface, (30, 143, 58),
          pygame.Rect(self.x - 28, self.y - 20, hpremain * 50, 10))

  def rotate(self):
    self.currentimg = pygame.transform.rotate(self.originalimg,
                                              hlp.radtodegrees(self.angle) - 90)
    
    self.shadowpic = pygame.transform.rotate(self.shadow,
                                              hlp.radtodegrees(self.angle) - 90)
    
  def draw(self, surface, tanklist):
    self.tankunsticker()
    self.maskimage = self.mask.to_surface()
    self.mask = pygame.mask.from_surface(self.currentimg)
    #surface.blit(self.maskimage,(self.x, self.y))
     
    #surface.blit(self.maskimage,((self.x - int(self.currentimg.get_width() / 2),
    #              self.y - int(self.currentimg.get_height() / 2 - 13))))
    if self.hp <= 0:
      self.currentimg = pygame.image.load("Crater.png")
      self.alive = False
      self.deadsfx.set_volume(1)
      self.deadsfx.play()
    if self.hp > 0:
      surface.blit(self.shadowpic,
                  (self.x - int(self.currentimg.get_width() / 2 - 4),
                    self.y - int(self.currentimg.get_height() / 2) + 16))
    surface.blit(self.currentimg,
                 (self.x - int(self.currentimg.get_width() / 2),
                  self.y - int(self.currentimg.get_height() / 2 - 12)))
    self.hpbar(surface)
    for b in self.bulletlist:
      b.draw(surface, tanklist, self.mineralslist)
    self.lastx = self.x
    self.lasty = self.y
    self.lastangle = self.angle
  def drawhitbox(self, surface):

    tank_rect = self.currentimg.get_rect(center=(self.x, self.y + 13))
    pygame.draw.rect(surface, pygame.Color(255, 0, 0), tank_rect)

  def takeinput(self, event):
    if event.type == pygame.KEYDOWN:
      if self.id == 0:
        if event.key == ord("w"):
          self.moveforward = 1
        if event.key == ord("a"):
          self.turnleft = -1
        if event.key == ord("s"):
          self.movebackward = -1
        if event.key == ord("d"):
          self.turnright = 1
        if event.key == pygame.K_LSHIFT:
          if self.alive and self.shootpossibility:
            bullet1 = Bullet(hlp.bulletstartoffsetx(self.x, self.angle),
                            hlp.bulletstartoffsety(self.y, self.angle) + 13,
                             self.angle, self, self.mineralslist)

            self.shoot(bullet1)
      if self.id == 1:
        if event.key == pygame.K_UP:
          self.moveforward = 1
        if event.key == pygame.K_DOWN:
          self.movebackward = -1
        if event.key == pygame.K_LEFT:
          self.turnleft = -1
        if event.key == pygame.K_RIGHT:
          self.turnright = 1
        if event.key == pygame.K_RSHIFT:
          if self.alive and self.shootpossibility:
            bullet2 = Bullet(hlp.bulletstartoffsetx(self.x, self.angle),
                              hlp.bulletstartoffsety(self.y, self.angle) + 13,
                              self.angle, self, self.mineralslist)
            self.shoot(bullet2)

    if event.type == pygame.KEYUP:
      if self.id == 0:
        if event.key == ord("a"):
          self.turnleft = 0
        if event.key == ord("d"):
          self.turnright = 0
        if event.key == ord("w"):
          self.moveforward = 0
        if event.key == ord("s"):
          self.movebackward = 0
      if self.id == 1:
        if event.key == pygame.K_UP:
          self.moveforward = 0
        if event.key == pygame.K_DOWN:
          self.movebackward = 0
        if event.key == pygame.K_LEFT:
          self.turnleft = 0
        if event.key == pygame.K_RIGHT:
          self.turnright = 0
  def movetank(self):
    # move body of this into draw, and have a self.moveforwardorback property
    self.moveforwardorback = self.moveforward + self.movebackward
    if self.moveforwardorback == 1:
      self.x += math.cos(self.angle) * self.speed
      self.y += math.sin(self.angle) * self.speed * -1
      for tank in self.tanklist:
        if tank.id != self.id:
          #if self.mask.overlap(tank.mask, ((self.x - int(tank.x)), self.y - (tank.y - tank.currentimg.get_height()))):
          if self.mask.overlap(tank.mask, ((tank.x - int(tank.currentimg.get_width() / 2)-(self.x - int(self.currentimg.get_width() / 2))), (tank.y - int(tank.currentimg.get_height() / 2 - tank.originalimg.get_width()/2) - (self.y - int(self.currentimg.get_height() / 2 - self.originalimg.get_width()/2))))):
            self.x += math.cos(self.angle) * self.speed * -1
            self.y += math.sin(self.angle) * self.speed
      for mineral in self.mineralslist:
        if self.mask.overlap(mineral.mask, ((mineral.x - (self.x - int(self.currentimg.get_width() / 2))), mineral.y - (self.y - int(self.currentimg.get_height() / 2 - self.originalimg.get_width()/2)))) :
            self.x += math.cos(self.angle) * self.speed * -1
            self.y += math.sin(self.angle) * self.speed
    if self.moveforwardorback == -1:
      self.x += math.cos(self.angle) * self.speed * -1
      self.y += math.sin(self.angle) * self.speed
      for tank in self.tanklist:
        if tank.id != self.id:
          #if self.mask.overlap(tank.mask, ((self.x - int(tank.x)), self.y - (tank.y - tank.currentimg.get_height()))):
          if self.mask.overlap(tank.mask, ((tank.x - int(tank.currentimg.get_width() / 2)-(self.x - int(self.currentimg.get_width() / 2))), (tank.y - int(tank.currentimg.get_height() / 2 - tank.originalimg.get_width()/2) - (self.y - int(self.currentimg.get_height() / 2 - self.originalimg.get_width()/2))))):
            self.x += math.cos(self.angle) * self.speed 
            self.y += math.sin(self.angle) * self.speed * - 1
      for mineral in self.mineralslist:
        if self.mask.overlap(mineral.mask, ((mineral.x - (self.x - int(self.currentimg.get_width() / 2))), mineral.y - (self.y - int(self.currentimg.get_height() / 2 - self.originalimg.get_width()/2)))) :
            self.x += math.cos(self.angle) * self.speed 
            self.y += math.sin(self.angle) * self.speed * -1
  def shoot(self, bullet):
    self.shootsfx.set_volume(1)
    self.shootsfx.play()
    bullet.damage = self.bulletdamage
    self.bulletlist.append(bullet)
    self.rtime = 0
  def reload(self,surface):
    self.rtime += 1
    if self.rtime >= self.reloadtime * 60:
      self.shootpossibility = True
    else:
      self.shootpossibility = False
      
    
    if self.alive:
      if 1 >= self.rtime/ (self.reloadtime * 60):
        self.reloadpercent = self.rtime / (self.reloadtime * 60)
      else:
        self.reloadpercent = 1
      pygame.draw.rect(
          surface, (128, 0, 0), pygame.Rect(self.x - 28, self.y - 35, 50, 10))
      pygame.draw.rect(
          surface, (234,255,58),
          pygame.Rect(self.x - 28, self.y - 35, self.reloadpercent * 50, 10))
  def tankunsticker(self):
          
    for tank in self.tanklist:
        if tank.id != self.id:
          if self.mask.overlap(tank.mask, ((tank.x - int(tank.currentimg.get_width() / 2)-(self.x - int(self.currentimg.get_width() / 2))), (tank.y - int(tank.currentimg.get_height() / 2 - tank.originalimg.get_width()/2) - (self.y - int(self.currentimg.get_height() / 2 - self.originalimg.get_width()/2))))):
            if self.turn != 0:
              self.angle += hlp.degreestorad(1) * self.speed / 2 * self.lastturndirection
    for mineral in self.mineralslist:
        if self.mask.overlap(mineral.mask, ((mineral.x - (self.x - int(self.currentimg.get_width() / 2))), mineral.y - (self.y - int(self.currentimg.get_height() / 2 - self.originalimg.get_width()/2)))) :
            if self.turn != 0:
              self.angle += hlp.degreestorad(1) * self.speed / 2 * self.lastturndirection
            
                    

  def tankturn(self):
    self.turn = self.turnleft + self.turnright
    if self.turn != 0:
      for tank in self.tanklist:
        if tank.id != self.id:
          if not self.mask.overlap(tank.mask, ((tank.x - int(tank.currentimg.get_width() / 2)-(self.x - int(self.currentimg.get_width() / 2))), (tank.y - int(tank.currentimg.get_height() / 2 - tank.originalimg.get_width()/2) - (self.y - int(self.currentimg.get_height() / 2 - self.originalimg.get_width()/2))))):
            self.lastturndirection = self.turn
    if self.turn == -1:
      

      self.angle += hlp.degreestorad(1) * self.speed/2
      
    if self.turn == 1:
      
      self.angle -= hlp.degreestorad(1) * self.speed/2
    

class Bullet:

  def __init__(self, x, y, angle, owner, mineralslist):
    self.x = x
    self.y = y
    self.speed = owner.bulletspeed
    self.damage = 0
    self.angle = angle
    self.owner = owner
    self.originalimg = pygame.image.load("tank bulet.png")
    self.currentimg = pygame.transform.scale(self.originalimg, (35 / 6, 13 / 6))
    self.imgsteptwo = pygame.transform.rotate(self.currentimg, hlp.radtodegrees(self.angle))
    self.bullethitsfx = pygame.mixer.Sound("Tankhitsfx.wav")
    self.bullethitsfx.set_volume(1)
    self.mask = pygame.mask.from_surface(self.imgsteptwo)
    self.mineralslist = mineralslist
    
    self.olist = 0
  def draw(self, surface, tanklist, mineralslist):
    self.x += math.cos(self.angle) * self.speed
    self.y += math.sin(self.angle) * -self.speed
    
    
   
    if self.speed != 0:
      surface.blit(self.imgsteptwo, (self.x, self.y))
      self.bullethitcheck(tanklist,self.mineralslist)

  def bullethitcheck(self, tanklist, mineralslist):
    self.masq = pygame.mask.from_surface(self.imgsteptwo)
    self.mask = self.masq.scale((self.speed,3))
    
    for tankindex, tank in enumerate(tanklist):
      (self.x - int(self.currentimg.get_width() / 2),
                  self.y - int(self.currentimg.get_height() / 2))
      
      if tank.mask.overlap(self.mask, ((self.x - int(tank.x - (tank.currentimg.get_width() / 2))), self.y - (tank.y - int(tank.currentimg.get_height() / 2  - 16)))):
        
        if tank.id == self.owner.id:
          break
        print("hit" + str(tankindex))
        self.hitmethod(tank)
    for mineral in self.mineralslist:
      if self.mask.overlap(mineral.mask, ((mineral.x - (self.x - int(self.currentimg.get_width() / 2))), mineral.y - (self.y - int(self.currentimg.get_height() / 2)))) :
        self.speed = 0

  def hitmethod(self, tankhit):
    self.speed = 0
    tankhit.hp -= self.owner.bulletdamage
    print(tankhit.hp)
    self.bullethitsfx.set_volume(1)
    self.bullethitsfx.play()
  def drawhitbox(self, surface):
    bullet_rect = self.imgsteptwo.get_rect(center=(self.x, self.y))
    print(bullet_rect)
    pygame.draw.rect(surface, (255, 87, 51), bullet_rect)