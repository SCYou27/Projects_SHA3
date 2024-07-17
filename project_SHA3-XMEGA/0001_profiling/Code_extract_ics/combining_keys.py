import numpy as np

def Z_rot_r(temp, Rnum):
  new = []
  for i in range(0, 64):
    new.append(temp[(((64-Rnum)+i)%64)])
  return new[:]

def forward():
  State = []
  for i in range(0, 25):
    Lane = []
    for bit in range(0, 64):
      Lane.append((i*8)+(bit//8))
    State.append(Lane)
  xRo = 1
  yRo = 0
  for itRo in range(0,24):
    temp = State[xRo+5*yRo]
    #print(xRo+5*yRo, temp)
    State[xRo+5*yRo] = Z_rot_r(temp, (itRo+1)*(itRo+2)//2)
    tempx = xRo
    xRo = yRo
    yRo = (2*tempx+3*yRo)%5
  tempState = State[:]
  for x in range(0,5):
    for y in range(0,5):
      State[x+5*y] = tempState[((x+3*y)%5)+5*x]
  combination = []
  for i in range(0, 200):
    t = []
    a = State[(i//8)][(8*(i%8)):8*(i%8+1)]
    for b in a:
      if t.count(b)==0:
        t.append(b)
    combination.append(t)
    #print(i, t, a)
  return combination

def backward():
  fore = forward()
  backsup = []
  for i in range(0, 200):
    backsup.append([])
  for f in range(0, 200):
    for t in range(0, len(fore[f])):
      backsup[fore[f][t]].append(f)
  for b in range(0, 200):
    backsup[b].sort()
  #for b in range(0, 200):
  #  print(b, '\t', backsup[b])
  return backsup

if __name__=='__main__':
  A = forward()
  B = backward()


