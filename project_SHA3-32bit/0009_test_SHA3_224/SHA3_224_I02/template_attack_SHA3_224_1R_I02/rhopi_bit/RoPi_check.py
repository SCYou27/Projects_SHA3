import numpy as np

def Z_rot_r(temp, Rnum):
  new = []
  for i in range(0, 64):
    new.append(temp[(((64-Rnum)+i)%64)])
  return new[:]

def main():
  State = []
  for i in range(0, 25):
    Lane = []
    for bit in range(0, 64):
      Lane.append((i*64)+bit)
    State.append(Lane)

  xRo = 1
  yRo = 0
  for itRo in range(0,24):
    temp = State[xRo+5*yRo]
    print xRo+5*yRo, temp
    State[xRo+5*yRo] = Z_rot_r(temp, (itRo+1)*(itRo+2)/2)
    tempx = xRo
    xRo = yRo
    yRo = (2*tempx+3*yRo)%5

  tempState = State[:]
  for x in range(0,5):
    for y in range(0,5):
      State[x+5*y] = tempState[((x+3*y)%5)+5*x]

  combination = []
  for bit in range(0, 1600):
    Lane = bit/64
    Zeta = bit%64
    t = State[Lane][Zeta]
    combination.append(t)
    print i, t
  np.save("foresupliment.npy", combination)
if __name__=='__main__':
  main()
