import numpy as np
import sys
str2num = {'0': 0, '1': 1, '2': 2, '3': 3,\
           '4': 4, '5': 5, '6': 6, '7': 7,\
           '8': 8, '9': 9, 'a':10, 'b':11,\
           'c':12, 'd':13, 'e':14, 'f':15 }

#Round constants for Keccak-f[1600]
RC = [ 0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,\
       0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,\
       0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,\
       0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,\
       0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,\
       0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008 ]

def hex2lane(value_hex):
  value_lanes = []
  hex_len = len(value_hex)//2
  lane = 0
  for t in range(0, hex_len):
    byte = 16*str2num[(value_hex[(2*t)])]+str2num[(value_hex[(2*t+1)])]
    lane ^= (byte<<(8*(t&0x7)))
    if (t&0x7==7):
      value_lanes.append(lane)
      lane = 0
  return value_lanes

def lane2hex(value_lanes):
  value_hex = ""
  for t in range(0, len(value_lanes)):
    temp = value_lanes[t]
    for b in range(0, 8):
      hex_v = hex((temp&0xff))[2:].strip('L').zfill(2)
      value_hex += hex_v
      temp >>= 8
  return value_hex

def Lane_Rotate(Lane, R):
  R = R&(2**6-1)
  Rotated = Lane<<R
  Output = (Rotated&(2**64-1))^(Rotated>>64)
  return Output

def Kec_f1600_inter(str_in, tag, rd):
  str_x = ""
  State = hex2lane(str_in)
  for it in range(0, 24):
    #Theta
    CB = [0]*5
    DB = [0]*5
    for x in range(0, 5):
      for y in range(0, 5):
        CB[x] ^= State[(x+5*y)]
    #== Output point: C ========================
    if (tag=='C')and(rd==it):
      str_x = lane2hex(CB)
    #===========================================
    for x in range(0, 5):
      pre = CB[int((x+4)%5)]
      lat = CB[int((x+1)%5)]
      lat = Lane_Rotate(lat, 1)
      DB[x] = pre^lat
    #== Output point: D ========================
    if (tag=='D')and(rd==it):
      str_x = lane2hex(DB)
    #===========================================
    for x in range(0, 5):
      for y in range(0, 5):
        State[(x+5*y)] ^= DB[x]
    #== Output point: E ========================
    if (tag=='E')and(rd==it):
      str_x = lane2hex(State)
    #===========================================
    #Pho
    x = 1
    y = 0
    for t in range(0, 24):
      R = int(((t+1)*(t+2))/2)&(2**6-1)
      L = x+5*y
      State[L] = Lane_Rotate(State[L], R)
      t_x = y
      t_y = (2*x+3*y)%5
      x = t_x
      y = t_y
    #Pi
    tempState = [0]*25
    for x in range(0, 5):
      for y in range(0, 5):
        x_old = (x+3*y)%5
        y_old = x
        tempState[(x+5*y)] = State[(x_old+5*y_old)]
    for i in range(0, 25):
      State[i] = tempState[i]
    #== Output point: A ========================
    if (tag=='A')and(rd==it):
      str_x = lane2hex(State)
    #===========================================
    #Chi
    tempState = [0]*25
    for x in range(0, 5):
      for y in range(0, 5):
        x1 = (x+1)%5
        x2 = (x+2)%5
        Lane1 = State[(x1+5*y)]^(2**64-1)
        Lane2 = State[(x2+5*y)]
        tempState[(x+5*y)] = Lane1&Lane2
    for i in range(0, 25):
      State[i] ^= tempState[i]
    #== Output point: B ========================
    if (tag=='B')and(rd==it):
      str_x = lane2hex(State)
    #===========================================
    #Iota
    State[0] ^= RC[it]
  str_out = lane2hex(State)
  return str_out, str_x
    
def find_intervalues(Tag, Rd):
  In = np.load("Invocation_IO/trace_input.npy")
  Out = np.load("Invocation_IO/trace_output.npy")
  Inter_Values = []
  if Tag=='A' or Tag=='B' or Tag=='E':
    Size = 400
  elif Tag=='C' or Tag=='D':
    Size = 80
  else:
    print("Error: wrong tag.")
    return
  for t in range(0, 64000):
    print("=================================================")
    print("Trace #"+str(t).zfill(6)+" "+Tag+str(Rd).zfill(2))
    Str_Out, Str_Inter = Kec_f1600_inter(In[t], Tag, Rd)
    if Str_Out!=Out[t]:
      print("Error: wrong output.")
      return
    if len(Str_Inter)!=Size:
      print("Error: wrong intermediate value size.")
      return
    Inter_Values.append(Str_Inter)
  intername = "Invocation_IO/intermediate_H_"+Tag+str(Rd).zfill(2)+".npy"
  np.save(intername, Inter_Values)
  return

if __name__=='__main__':
  Tags = ['A', 'B', 'C', 'D', 'E']
  for tag in Tags:
    for round_index in range(0, 4):
      find_intervalues(tag, round_index)

