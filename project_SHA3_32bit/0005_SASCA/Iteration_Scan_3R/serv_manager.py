import numpy as np
import os
import time
def Wait():
  print("Try again later.")
  time.sleep(300)
  return

def Open(name, S):
  while True:
    try:
      Obj = open(name, S)
    except:
      Wait()
      continue
    break
  return Obj

def Load(name):
  while True:
    try:
      Obj = np.load(name)
    except:
      Wait()
      continue
    break
  return Obj

def Save(name, Obj):
  while True:
    try:
      np.save(name, Obj)
    except:
      Wait()
      continue
    break
  return

def System(cmd):
  while os.system(cmd):
    Wait()
  return

