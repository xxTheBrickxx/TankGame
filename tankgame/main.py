import random
import pygame
import math
import sys
import time

from tank import *
import helper as hlp

#procederal placement algorithms
#poisson disc sampling
#object collision, tanks and bullets should not go through terrain


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
pygame.mixer.init()
screen_w = 1050
screen_h = 450
WIN = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)
pygame.display.set_caption("Tanks")

clock = pygame.time.Clock()
fps = 60
frames = 0

tanklist = []
ogtank = {
    "name": "og tank",
    "image": "ogtank.png",
    "speed": 2,
    "hp": 1000,
    "bulletspeed": 1,
    "bulletdamage": 250,
    "reloadtime": 3
}
greenmonstertank = {
    "name": "monster tank",
    "image": "greenmonstertank.png",
    "speed": 10,
    "hp": 200,
    "bulletspeed": 20,
    "bulletdamage": 50,
    "reloadtime": 2
}
littletank = {
    "name": "little tank",
    "image": "little tank.png",
    "speed": 15,
    "hp": 50,
    "bulletspeed": 20,
    "bulletdamage": 10,
    "reloadtime": 1
}
longgraytank = {
    "name": "The Grey Guy",
    "image": "long gray tank.png",
    "speed": 15,
    "hp": 50,
    "bulletspeed": 20,
    "bulletdamage": 10,
    "reloadtime": 1
}
mediumtank = {
    "name": "The Myth",
    "image": "medium tank.png",
    "speed": 15,
    "hp": 50,
    "bulletspeed": 20,
    "bulletdamage": 10,
    "reloadtime": 1
}
thebigtank = {
    "name": "Godzilla",
    "image": "thebigtank.png",
    "speed": 15,
    "hp": 50,
    "bulletspeed": 20,
    "bulletdamage": 10,
    "reloadtime": 1
}
tankselectmat = [[ogtank, greenmonstertank, littletank],
                 [longgraytank, mediumtank, thebigtank]]


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
        return ("done")
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
    surface.fill(pygame.Color(140, 140, 140))
    font = pygame.font.Font("DTM-Mono.otf", 42)
    text = font.render("select tank:", True, (30, 125, 20))
    text_rect = text.get_rect(center=(screen_w / 2, screen_h / 10))
    surface.blit(text, text_rect)

    for i in range(len(tankselectmat[0])):
      for j in range(len(tankselectmat)):
        tanki = pygame.image.load(tankselectmat[j][i]["image"])
        recti = tanki.get_rect(center=((screen_w - 400) / 3 * (i + 1.5) -
                                       12 / 2, 100 * (j + 2) - 6))
        recti.width += 12
        recti.height += 12
        selectedtank = pygame.image.load(tankselectmat[tankselecty1][tankselectx1]["image"]).convert_alpha()
        selectedtank2 = pygame.transform.scale(selectedtank, (selectedtank.get_width() * 3, selectedtank.get_height() * 3))
        surface.blit(selectedtank2, (100 - selectedtank2.get_width()/2, 150 -  selectedtank2.get_height()/2))
        selectedtank3 = pygame.image.load(tankselectmat[tankselecty2][tankselectx2]["image"]).convert_alpha()
        selectedtank4 = pygame.transform.scale(selectedtank3, (selectedtank3.get_width() * 3, selectedtank3.get_height() * 3))
        surface.blit(selectedtank4, (900 - selectedtank4.get_width()/2, 150 -  selectedtank4.get_height()/2))                                       
        if i == tankselectx1 and j == tankselecty1 and i == tankselectx2 and j == tankselecty2:
          c = (75, 0, 130)
        elif i == tankselectx1 and j == tankselecty1:
          c = (255, 0, 0)
        elif i == tankselectx2 and j == tankselecty2:
          c = (0, 0, 255)
        else:
          c = (140, 140, 140)

        pygame.draw.rect(surface, c, recti)
        surface.blit(tanki, ((screen_w - 400) / 3 * (i + 1.5) -
                             (tanki.get_width() / 2), 100 * (j + 2) -
                             (tanki.get_height() / 2)))

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
        if event.key == ord("s") and tankselecty1 == 0:
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
          return tankwanted, tankwanted2

      quitfunction(event)


def tankbattle(surface, tanks):

  pygame.display.set_caption("Battle")
  frames = 0
  turn = 0

  tank1 = Tank(tanks[0], 250, 250, hlp.degreestorad(0), 0)
  tank2 = Tank(tanks[1], 750, 250, hlp.degreestorad(180), 1)

  tanklist.append(tank1)
  tanklist.append(tank2)
  running = True
  while running:
    clock.tick(fps)
    frames += 1
    print(frames)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          pygame.quit()
          sys.exit()

      tank1.takeinput(event)
      tank2.takeinput(event)

    if turn == 1:
      tank1.angle += hlp.degreestorad(1)
    if turn == 2:
      tank1.angle -= hlp.degreestorad(1)

    surface.fill(pygame.Color("#ECD796"))

    if tank1.alive:

      tank1.movetank()
      tank1.rotate()
      tank1.tankturn()
      tank1.reload(WIN)
    if tank2.alive:
      tank2.movetank()
      tank2.rotate()
      tank2.tankturn()
      tank2.reload(WIN)
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

    tank1.draw(surface, tanklist)
    tank2.draw(surface, tanklist)
    pygame.display.update()

  while True:
    print("done")
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          tanklist.clear()
          return ("done")
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
  print(tankbattle(WIN, tankselect(WIN)))
pygame.quit()
sys.exit()

# _ tank stats dictionary
# _ menu screen functionality

# example dictionary
# tankstats = { "hp" : 100, "damage" : 10, "image" : image_file}
