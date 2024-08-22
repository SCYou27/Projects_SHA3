import KECCAK
import Three_Layer
import numpy as np

State = [0x8765384678e2169f, 0x0568374e4e21b1f7, 0x4f7e280c8478de94, 0x4b96d0e64bde10b1, 0x274b8a5ef0aae734, \
         0x46e48b1c5c195126, 0x5f7cf75ded311e45, 0xcf046b869d6ecfd4, 0x37311fefd97b3ab2, 0x7d0275f1fd404e0a, \
         0xdc585f0acfe7e83d, 0xea4e71cb2be8c839, 0xcb4fcd185531ff11, 0xc048771cd6fa6d5a, 0xd8c7a68a6b2a3518, \
         0x8b46bbaba823a6a4, 0xf6a6c13f4c69f24f, 0xdcbc34eacc266740, 0x2fe5d017ede297df, 0x95e714b2b89dd109, \
         0x2c36c927144e76d4, 0x08b8d9044927a433, 0xe208fa08f6aa3a21, 0x418c29cdcdbcb9bb, 0xeec3a7ce3af804b6]

State1 = KECCAK.Chi(State[:])

st0 = Three_Layer.ChiByteRow(State[ 0: 5])
st1 = Three_Layer.ChiByteRow(State[ 5:10])
st2 = Three_Layer.ChiByteRow(State[10:15])
st3 = Three_Layer.ChiByteRow(State[15:20])
st4 = Three_Layer.ChiByteRow(State[20:25])

State2 = st0+st1+st2+st3+st4

def byte2hex(byte):
  return '0x'+hex(byte&0xff)[2:].zfill(2)

def lane2hex(lane):
  return '0x'+hex(lane)[2:].zfill(16)

for t in range(0, 25):
  print(lane2hex(State[t]), lane2hex(State1[t]), byte2hex(State2[t]))

State3 = KECCAK.Theta(KECCAK.Iota(KECCAK.Chi(State[:])[:], 0)[:])

State4 = Three_Layer.ChiIotaThetaByteSlice(State[:], 0)

print('======================================================================================')

for t in range(0, 25):
  print(lane2hex(State[t]), lane2hex(State3[t]), byte2hex(State4[t]))
