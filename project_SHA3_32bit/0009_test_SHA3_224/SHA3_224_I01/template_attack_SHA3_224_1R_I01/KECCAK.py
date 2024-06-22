#################################################################################################
#
# Written by Shih-Chun You (scy27@cam.ac.uk)
# Version 3: 2021 MAY 26
#
# For both Python2 and Python3.
# No dependent libraries.
#
# Usage:
#
#   SHA3 functions:
#
#     KECCAK.SHA3_224(M)
#     KECCAK.SHA3_256(M)
#     KECCAK.SHA3_384(M)
#     KECCAK.SHA3_512(M)
#
#   SHAKE extended output functions:
#
#     KECCAK.SHAKE128(M, B)
#     KECCAK.SHAKE256(M, B)
#
#   M: hexadecimal input message with arbitrary length.
#   B: arbitrary-length output size in bytes.
#
#   Main function:
#
#     python KECCAK.py
#
#     print if KECCAK.SHA3_224("00") correct?
#     print if KECCAK.SHA3_256("00") correct?
#     print if KECCAK.SHA3_384("00") correct?
#     print if KECCAK.SHA3_512("00") correct?
#     print if KECCAK.SHAKE128("00", 32) correct?
#     print if KECCAK.SHAKE256("00", 32) correct?
#
################################################################################################
#
# Update 2021/03/22:
#
#   Add inverse functions
#
# Update 2021/05/26:
# 
#   Revise int(len(value_hex)/2) => len(value_hex)//2
#
#
#
#################################################################################################


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

def Mod_p(number):
  while(number>(2**64-1)):
    high = number>>64
    low = number&(2**64 - 1)
    number = low^high
  return number

def Gal_mult(num1, num2):
  result = 0
  W = 2**64
  while(W):
    result = result<<1
    if W&num2:
     result ^= num1
    W = W>>1
  return Mod_p(result)


def Back_Theta(State):
  Output = [0]*25
  Inv_Constant = [0]*5
  Inv_Constant[0] = 0xDE26BC4D789AF134
  Inv_Constant[1] = 0x09AF135E26BC4D78
  Inv_Constant[2] = 0xEBC4D789AF135E26
  Inv_Constant[3] = 0x7135E26BC4D789AF
  Inv_Constant[4] = 0xCD789AF135E26BC4
  C = [0]*5
  for y in range(0, 5):
    for x in range(0, 5):
      C[x] ^= State[(x+5*y)]
  D = [0]*5
  for x in range(0, 5):
    for x0 in range(0, 5):
      D[x] ^= Gal_mult(Inv_Constant[((5-x0)%5)], C[((x+x0)%5)])
  for y in range(0, 5):
    for x in range(0, 5):
      Output[x+5*y] = State[x+5*y]^D[x]
  return Output

def Back_RhoPi(State):
  Output = [0]*25
  #Pi
  for x in range(0,5):
    for y in range(0,5):
      Output[((x+3*y)%5)+5*x] = State[x+5*y]
  #Ro 
  xRo = 1
  yRo = 0
  for itRo in range(0,24):
    temp = Output[xRo+5*yRo]
    robit = ((itRo+1)*(itRo+2)//2)%64
    Output[xRo+5*yRo] = Lane_Rotate(temp, (64-robit))
    tempx = xRo
    xRo = yRo
    yRo = (2*tempx+3*yRo)%5
  return Output

def Back_Chi(State):
  Output = []
  NOT_NUM = (2**64-1)
  for y in range(0,5):
    for x in range(0,5):
      t = []
      for i in range(0,5):
        t.append(State[((x+i)%5)+5*y])
      temp1 = t[0]&t[1]
      temp2 = ((NOT_NUM^t[4])&(NOT_NUM^t[1]))&(t[0]^t[2])
      temp3 = t[4]&(NOT_NUM^t[1])
      temp4 = temp3&(((NOT_NUM^t[0])^t[2])^t[3])
      Output.append((temp1|temp2)|temp4)
  return Output

def Back_Iota(State, Omega):
  State[0] ^= RC[Omega]
  return State

def Theta(State):
  CB = [0]*5
  DB = [0]*5
  for x in range(0, 5):
    for y in range(0, 5):
      CB[x] ^= State[(x+5*y)]
  for x in range(0, 5):
    pre = CB[int((x+4)%5)]
    lat = CB[int((x+1)%5)]
    lat = Lane_Rotate(lat, 1)
    DB[x] = pre^lat
  for x in range(0, 5):
    for y in range(0, 5):
      State[(x+5*y)] ^= DB[x]
  return State

def RhoPi(State):
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
  return State

def Chi(State):
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
  return State

def Iota(State, it):
  State[0] ^= RC[it]
  return State
    

def Keccak_f1600(State):
  for it in range(0, 24):
    State = Theta(State)
    State = RhoPi(State)
    State = Chi(State)
    State = Iota(State, it)
  return State

def Back_Keccak_f1600(State):
  for it in range(0, 24):
    State = Back_Iota(State, (23-it))
    State = Back_Chi(State)
    State = Back_RhoPi(State)
    State = Back_Theta(State)
  return State



def Keccak_sp(capacity, Lanes, d):
  Output = []
  rate = 1600-capacity
  rate_lane = rate>>6
  T_absorb = int((len(Lanes)/rate_lane))
  T_squeeze = int((d/rate))
  if d%rate!=0:
    T_squeeze+=1
  State = [0]*25
  # Absorbing stage
  for t in range(0, T_absorb):
    for L in range(0, rate_lane):
      State[L] ^= Lanes[(t*rate_lane+L)]
    State = Keccak_f1600(State)
  # Squeezing stage
  for t in range(0, T_squeeze):
    for L in range(0, rate_lane):
      Output.append(State[L])
    State = Keccak_f1600(State)
  return Output

def padding_SHA3(M, rate):
  M_len = int(len(M)/2)
  rate_B = rate>>3
  pad_size = rate_B-(M_len%rate_B)
  if pad_size==1:
    Output = M+"86"
  else:
    Output = M+"06"
    for t in range(0, pad_size-2):
      Output += "00"
    Output += "80"
  return Output 

def padding_SHAKE(M, rate):
  M_len = int(len(M)/2)
  rate_B = rate>>3
  pad_size = rate_B-(M_len%rate_B)
  if pad_size==1:
    Output = M+"9f"
  else:
    Output = M+"1f"
    for t in range(0, pad_size-2):
      Output += "00"
    Output += "80"
  return Output

def SHA3(d, M):
  if (d==224)or(d==256)or(d==384)or(d==512):
    capacity = 2*d
    rate = 1600-capacity
    N = padding_SHA3(M, rate)
    #print("DEBUG: after padding = ", N)
    Input = hex2lane(N)
    #for t in range(0, len(Input)):
    #  print("DEBUG: lane", t, hex(Input[t]))
    Output = Keccak_sp(capacity, Input, d)
    Out_hex = lane2hex(Output)
    #print("DEBUG: Out_hex = ", Out_hex)
    Out_trunc = Out_hex[0:(d>>2)]
    return Out_trunc
  else:
    print("Undefined size of SHA3:", d)
    return "XX"

def SHAKE(s, M, d):
  if (s==128)or(s==256):
    capacity = 2*s
    rate = 1600-capacity
    N = padding_SHAKE(M, rate)
    Input = hex2lane(N)
    Output = Keccak_sp(capacity, Input, d)
    Out_hex = lane2hex(Output)
    Out_trunc = Out_hex[0:(d>>2)]
    return Out_trunc
  else:
    print("Undefined size of SHAKE:", s)
    return "XX"

def SHA3_224(M):
  return SHA3(224, M)

def SHA3_256(M):
  return SHA3(256, M)

def SHA3_384(M):
  return SHA3(384, M)

def SHA3_512(M):
  return SHA3(512, M)

def SHAKE128(M, B):
  #B: output size in bytes.
  return SHAKE(128, M, (B*8))

def SHAKE256(M, B):
  #B: output size in bytes.
  return SHAKE(256, M, (B*8))


if __name__=='__main__':
  ANS0 = "bdd5167212d2dc69665f5a8875ab87f23d5ce7849132f56371a19096"
  ANS1 = "5d53469f20fef4f8eab52b88044ede69c77a6a68a60728609fc4a65ff531e7d0"
  ANS2 = "127677f8b66725bbcb7c3eae9698351ca41e0eb6d66c784bd28dcdb3b5fb12d0c8e840342db03ad1ae180b92e3504933"
  ANS3 = "7127aab211f82a18d06cf7578ff49d5089017944139aa60d8bee057811a15fb55a53887600a3eceba004de51105139f32506fe5b53e1913bfa6b32e716fe97da"
  ANS4 = "0b784469a0628e03861cd8a196dfafa0e9e8056d04cddcc49f0746b9ad43ccb2"
  ANS5 = "b8d01df855f7075882c636f6ddeacf41e5de0bbf30042ef0a86e36f4b8600d54"
  print(ANS0==SHA3_224("00"))
  print(ANS1==SHA3_256("00"))
  print(ANS2==SHA3_384("00"))
  print(ANS3==SHA3_512("00"))
  print(ANS4==SHAKE128("00", 32))
  print(ANS5==SHAKE256("00", 32))
