import numpy as np
import enumeration


def ChiByteRow(State):
  tempState = [0]*5
  for x in range(0, 5):
    x1 = (x+1)%5
    x2 = (x+2)%5
    Lane1 = ((State[x1]&255)^255)
    Lane2 = (State[x2]&255)
    tempState[x] = (Lane1&Lane2)
  Out = []
  for x in range(0, 5):
    Out.append((State[x]^tempState[x])&255)
  return Out

def ChiIotaThetaByteSlice(State, z):
  ## Chi ######################################
  ChiState = []
  for y in range(0, 5):
    ChiState += ChiByteRow(State[(y*5):(y*5+5)])
  ## Iota #####################################
  if z==0:
    ChiState[0] = ChiState[0]^0x01
  ## Theata ##################################
  C_state = []
  for x in range(0, 5):
    C_state.append(ChiState[0*5+x]^ChiState[1*5+x]^ChiState[2*5+x]^ChiState[3*5+x]^ChiState[4*5+x])
  D_state = []
  for x in range(0, 5):
    D_state.append((C_state[(x+4)%5]^(C_state[(x+1)%5]<<1))&0xff) # Assume Tau = 0
  Out = []
  for y in range(0, 5):
    for x in range(0, 5):
      Out.append((ChiState[y*5+x]^D_state[x])&0xff)
  return Out

def Byte2LaneState(Candidates):
  State = []
  for y in range(0, 5):
    for x in range(0, 5):
      Lane = 0
      for z in range(0, 8):
        Lane += Candidates[(z*25+y*5+x)]*(256**z)
      State.append((Lane&(2**64-1)))
  return State
  

class ThreeLayerSearcher:
  def __init__(self, Table_A, Table_B, Table_E):
    self.Table_A = Table_A
    self.Table_B = Table_B
    self.Table_E = Table_E
    return

  def search(self, Cap_LV1=2500, Cap_LV2=2500, Cap_LV3=1):
    print('Cap_LV1 = '+str(Cap_LV1)+', Cap_LV2 = '+str(Cap_LV2)+', Cap_LV3 = '+str(Cap_LV3))
    Tables_LV1 = []
    Tables_LV2 = []
    Tables_LV3 = []
    ## Level 1 ###################################################################
    print('Level 1')
    for z in range(0, 8):
      for y in range(0, 5):
        #print('Row '+str(z*5+y).zfill(2))
        ByteRowTable = []
        Enumerator = enumeration.Enumerator([self.Table_A[(y*40+0*8+z)], \
                                             self.Table_A[(y*40+1*8+z)], \
                                             self.Table_A[(y*40+2*8+z)], \
                                             self.Table_A[(y*40+3*8+z)], \
                                             self.Table_A[(y*40+4*8+z)]])
        for it in range(0, Cap_LV1):
          candidates, dist = Enumerator.Next_one()
          cand_B = ChiByteRow(candidates)
          for x in range(0, 5):
            dist += self.Table_B[(y*40+x*8+z)][cand_B[x]][1]
          ByteRowTable.append([candidates[:], dist])
        Tables_LV1.append(ByteRowTable)
    ## Level 2 ###################################################################
    print('Level 2')
    for z in range(0, 8):
      ByteSliceTable = []
      #print('Slice '+str(z).zfill(2))
      Enumerator = enumeration.Enumerator(Tables_LV1[(z*5):(z*5+5)])
      for it in range(0, Cap_LV2):
        candidates, dist = Enumerator.Next_one()
        cand_E = ChiIotaThetaByteSlice(candidates, z)
        for x in range(0, 5):
          dist0 = 0.0
          dist1 = 0.0
          for y in range(0, 5):
            dist0 += self.Table_E[(y*40+x*8+z)][cand_E[y*5+x]][1]
            dist1 += self.Table_E[(y*40+x*8+z)][(cand_E[y*5+x])^0x01][1]
          dist += min(dist0, dist1)
        ByteSliceTable.append([candidates[:], dist])
      Tables_LV2.append(ByteSliceTable)
    ## Level 3 ###################################################################
    print('Level 3')
    Enumerator = enumeration.Enumerator(Tables_LV2)
    for it in range(0, Cap_LV3):
      candidates, _ = Enumerator.Next_one()
      Tables_LV3.append(Byte2LaneState(candidates))
    return Tables_LV3


