import random
import pygame
import math
import sys
import time

import tank
import helper as hlp


def quitfunction(event):
  if event.type == pygame.QUIT:
    pygame.quit()
    sys.exit()
  if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
    pygame.quit()
    sys.exit()
#bullet 35,13
#tank 24,60





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
    "name" : "og tank",
    "image": "ogtank.png",
    "speed": 5,
    "hp": 100,
    "bulletspeed": 10,
    "bulletdamage": 25,
    "reloadtime": 1
}
greenmonstertank = {
  "name" : "monster tank",
  "image" : "greenmonstertank.png",
  "speed" : 10,
  "hp" : 200,
  "bulletspeed" : 20,
  "bulletdamage" : 50,
  "reloadtime" : 2
}
littletank = {
  "name" : "little tank",
  "image" : "little tank.png",
  "speed" : 15,
  "hp" : 50,
  "bulletspeed" : 20,
  "bulletdamage" : 10,
  "reloadtime" : 1
}
longgraytank= {
  "name" : "The Grey Guy",
  "image" : "long gray tank.png",
  "speed" : 15,
  "hp" : 50,
  "bulletspeed" : 20,
  "bulletdamage" : 10,
  "reloadtime" : 1
}
mediumtank = {
  "name" : "The Myth",
  "image" : "medium tank.png",
  "speed" : 15,
  "hp" : 50,
  "bulletspeed" : 20,
  "bulletdamage" : 10,
  "reloadtime" : 1
}
thebigtank = {
  "name" : "Godzilla",
  "image" : "thebigtank.png",
  "speed" : 15,
  "hp" : 50,
  "bulletspeed" : 20,
  "bulletdamage" : 10,
  "reloadtime" : 1
}
tankselectmat = [[ogtank,greenmonstertank,littletank],[longgraytank,mediumtank,thebigtank]]

#self,x,y,speed,angle,img,hp,id,bulletspeed=10,bulletdamage=25,reloadtime=1
def gamestartmenu(surface):
  while True:
    surface.fill(pygame.Color(0, 0, 0))
    font = pygame.font.Font("DTM-Mono.otf", 28)
    text = font.render("Press space to begin", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen_w / 2, screen_h / 2))
    surface.blit(text, text_rect)
    pygame.display.update()
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
          return("done")
      quitfunction(event)
def tankselect(surface):
  tankselecty1 = 0
  tankselectx1 = 0
  tankselecty2 = 0
  tankselectx2 = 0

  p1tf = False
  p2tf = False

  while True:


    #color is (148,148,148)
    #screen_w = 1050
    #screen_h = 450
    surface.fill(pygame.Color(140,140,140))
    font = pygame.font.Font("DTM-Mono.otf", 42)
    text = font.render("select tank:", True, (30, 125, 20))
    text_rect = text.get_rect(center=(screen_w / 2, screen_h / 10))
    surface.blit(text, text_rect)

    for i in range(len(tankselectmat[0])):
      for j in range(len(tankselectmat)):
        tanki = pygame.image.load(tankselectmat[j][i]["image"])
        recti = tanki.get_rect(center = ((screen_w - 400)/3 * (i+1.5) - 10/2, 100 * (j+2)-5))
        recti.width += 10
        recti.height += 10

        if i == tankselectx1 and j == tankselecty1 and i == tankselectx2 and j == tankselecty2:
          c = (75,0,130)
        elif i == tankselectx1 and j == tankselecty1:
          c = (255,0,0)
        elif i == tankselectx2 and j == tankselecty2:
          c = (0,0,255)
        else:
          c = (140,140,140)
          
        
        pygame.draw.rect(surface, c, recti)
        surface.blit(tanki,((screen_w - 400)/3 * (i+1.5) - (tanki.get_width()/2),100 * (j+2) - (tanki.get_height()/2)))
       
    # displays the selcted tank stats

    pygame.display.update()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYDOWN:

        if event.key == ord("w") and tankselecty1 == 1:
          tankselecty1 -= 1
        if event.key == ord("a") and tankselectx1 >= 1:
          tankselectx1 -= 1
        if event.key == ord("s") and tankselecty1 ==0:
          tankselecty1 += 1
        if event.key == ord("d") and tankselectx1 <= 1:
          tankselectx1 += 1
        if event.key == pygame.K_LSHIFT:
          p1tf = True

        if event.key == pygame.K_UP and tankselecty2 == 1:
          tankselecty2 -= 1
        if event.key == pygame.K_DOWN and tankselecty2 == 0:
          tankselecty2 += 1
        if event.key == pygame.K_LEFT and tankselectx2 >= 1:
          tankselectx2 -= 1
        if event.key == pygame.K_RIGHT and tankselectx2 <= 1:
          tankselectx2 += 1
        if event.key == pygame.K_RSHIFT:
          p2tf = True
        if event.key == pygame.K_SPACE:
          tankwanted = tankselectmat[tankselecty1][tankselectx1]
          tankwanted2 = tankselectmat[tankselecty2][tankselectx2]
          return tankwanted , tankwanted2 

      quitfunction(event)
def tankbattle(surface,tanks):



  pygame.display.set_caption("Battle")

  turn = 0

  tank1 = tank.Tank(tanks[0],
               250,
               250,
               hlp.degreestorad(0),
               0)
  tank2 = tank.Tank(tanks[1],
               750,
               250,
               hlp.degreestorad(180),
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
            bullet1 = tank.Bullet(hlp.bulletstartoffsetx(tank1.x, tank1.angle),
                             hlp.bulletstartoffsety(tank1.y, tank1.angle) + 13, 10,
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
            bullet2 = tank.Bullet(hlp.bulletstartoffsetx(tank2.x, tank2.angle),
                             hlp.bulletstartoffsety(tank2.y, tank2.angle) + 13, 10,
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
      tank1.angle += hlp.degreestorad(1)
    if turn == 2:
      tank1.angle -= hlp.degreestorad(1)

    surface.fill(pygame.Color("#ECD796"))

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
      draw_gameover2(surface)
      running = False
    if not tank2.alive:
      for b in tank2.bulletlist:
        b.speed = 0
      draw_gameover(surface)
      running = False

    tank1.draw(surface,tanklist)
    tank2.draw(surface,tanklist)
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
    surface.blit(prespace, prespacetext_rect)
    pygame.display.update()



while True:
  gamestartmenu(WIN)
  print(tankbattle(WIN,tankselect(WIN)))
pygame.quit()
sys.exit()

# _ tank stats dictionary
# _ menu screen functionality

# example dictionary
# tankstats = { "hp" : 100, "damage" : 10, "image" : image_file}