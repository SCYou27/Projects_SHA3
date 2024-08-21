import numpy as np
import get_tables as template
import serv_manager as svm
import KECCAK as KEC
import Three_Layer
import os
import sys
import h5py
import time

###################################################################################
#
# Independent parameters
#
# SHA Size:
D_Size = 512
# Invocation number:
INVOC = 1
Tr_NUM = 100
# Set lower and upper bounds:
SET_L = 0
SET_U = 10
###################################################################################
C_Size = 2*D_Size
R_Size = 1600-C_Size
Project_Tag = 'SHA3_'+str(D_Size)+'_I'+str(INVOC).zfill(2)+'_'
PPC = 25

class Template_Recover:
  def __init__(self):
    self.Template_A00 = template.Template('A00')
    self.Template_B00 = template.Template('B00')
    self.Template_E01 = template.Template('E01')
    return
  
  def recovering(self, trace):
    T_A = self.Template_A00.Guess(trace)
    T_B = self.Template_B00.Guess(trace)
    T_E = self.Template_E01.Guess(trace)
    return T_A, T_B, T_E

def Invocational_IO(StateA00):
  temp0 = KEC.Back_RhoPi(StateA00)
  temp1 = KEC.Back_Theta(temp0)
  cal_stringH = KEC.lane2hex(temp1)
  Start = R_Size//4
  Next = KEC.Keccak_f1600(KEC.hex2lane(cal_stringH))
  return temp1, Next

def Consistent_Check(Pre, InS):
  stateA = np.array(Pre[(R_Size//64):], dtype=np.uint64)
  stateB = np.array(InS[(R_Size//64):], dtype=np.uint64)
  return np.array_equiv(stateA, stateB)

def Keccak_input_strip(kec_in):
  if kec_in[-2:]=='86':
    output = kec_in[:-2]
    return output
  elif kec_in[-2:]=='80':
    tmp = kec_in[:-2]
    while(tmp[-2:]=='00'):
      tmp = tmp[:-2]
    if tmp[-2:]=='06':
      output = tmp[:-2]
      return output
  return 'Wrong_In'

class Recovery:
  def __init__(self):
    print('Loading answer strings...')
    self.ans_inputs = []
    for t in range(SET_L, SET_U):
      ans_name = 'data_raw_in/set_I'+str(INVOC).zfill(2)+'_'+str(t).zfill(4)+'_inputs.npy'
      string_inputs = svm.Load(ans_name)
      for s in range(0, len(string_inputs)):
        self.ans_inputs.append(string_inputs[s])
    print('Template initializing...')
    self.TA = Template_Recover()
    self.TRACE_FILES = []
    for invoc in range(0, INVOC):
      fname = '../Processed_HDF5/Invocation_'+str(invoc).zfill(2)+'.hdf5'
      print('Loading traces from '+fname)
      self.TRACE_FILES.append(h5py.File(fname, 'r'))
    return
  
  def close(self):
    for invoc in range(0, INVOC):
      self.TRACE_FILES[invoc].close()
    return
  
  def recover(self, tr):
    print('======================================================')
    print('SHA3_input #'+str(tr).zfill(2), time.asctime())
    print('======================================================')
    tS = time.time()
    rec_IN = ''
    prev = [0]*25
    Caps = [-1]*INVOC
    Suc_state = True
    for invoc in range(0, INVOC):
      trace = self.TRACE_FILES[invoc]['Traces'][tr][()]
      print('Template attack...')
      Table_A, Table_B, Table_E = self.TA.recovering(trace)
      print('Three-layer searching...')
      Search_3L = Three_Layer.ThreeLayerSearcher(Table_A, Table_B, Table_E)
      Capacity = 2500
      while Capacity<2560000:
        A00_Table = Search_3L.search(Cap_LV1=Capacity, Cap_LV2=Capacity, Cap_LV3=1)
        inv_in, inv_out = Invocational_IO(A00_Table[0])
        if Consistent_Check(prev, inv_in):
          print('Consistence check passed!')
          IN_XOR_bin = []
          for lane in range(0, 25):
            IN_XOR_bin.append(inv_in[lane]^prev[lane])
          IN_XOR_hex = KEC.lane2hex(IN_XOR_bin)
          rec_IN += (IN_XOR_hex[:(R_Size//4)])
          prev = inv_out[:]
          break
        Capacity *= 4
      Caps[invoc] = Capacity
      if Capacity==2560000:
        print('Search failed!')
        rec_IN = 'Not Found!'
        break 
    rec_IN = Keccak_input_strip(rec_IN)
    tE = time.time()
    print(('Prediction: '+rec_IN))
    print(('Answer    : '+self.ans_inputs[tr]))
    print(('Wall time : '+str(tE-tS)))
    pred_name = './Recovered_Data/recovered_inputs_'+str(tr).zfill(4)+'.npy'
    svm.Save(pred_name, rec_IN)
    caps_name = './Capacities/capacity_'+str(tr).zfill(4)+'.npy'
    svm.Save(caps_name, Caps)
    succ_name = './Success/success_'+str(tr).zfill(4)+'.npy'
    Success = (rec_IN==self.ans_inputs[tr])
    svm.Save(succ_name, Success)
    return Success

def Attack(L, U):
  Attacker = Recovery()
  Suc = []
  for t in range(L, U):
    Suc.append(Attacker.recover(t))
  Attacker.close()
  return Suc

if __name__=='__main__':
  lower = int(sys.argv[1])
  upper = int(sys.argv[2])
  Success = Attack(lower, upper)
  print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
  print('Results:')
  print('Total  : '+str(len(Success)))
  print('Success: '+str(Success.count(True)))

