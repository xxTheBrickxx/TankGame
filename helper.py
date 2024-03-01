import math

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