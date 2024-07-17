import numpy as np
import get_tables as template
import marginalization
import SASCA_scan
import serv_manager as svm
import KECCAK as KEC
import os
import sys
import h5py

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
P_N = [0.5, 0.5]
P_0 = [1.0, 0.0]
P_1 = [0.0, 1.0]
Project_Tag = 'SHA3_'+str(D_Size)+'_I'+str(INVOC).zfill(2)+'_'
PPC = 25

class Template_Recover:
  def __init__(self):
    self.Template_A00 = template.Template('A00')
    self.Template_B00 = template.Template('B00')
    self.Template_E01 = template.Template('E01')
    self.Template_B01 = template.Template('B01')
    self.ZeroIN = []
    self.Marginalizer = marginalization.Marginalization(8, False)
    return
  
  def in_table(self, State):
    Bits = []
    bit_IN = []
    for lane in range(0, 25):
      for k in range(0, 64):
        if (State[lane]&(2**k))==0:
          Bits.append(0)
        else:
          Bits.append(1)
    for t in range(0, R_Size):
      bit_IN.append(P_N)
    for t in range(R_Size, 1600):
      if Bits[t]==0:
        bit_IN.append(P_0)
      else:
        bit_IN.append(P_1)
    return np.transpose(np.array(bit_IN))
  
  def recovering(self, trace, pre_inputs):
    b_A = []
    b_B = []
    b_A.append(self.Marginalizer.marginalize(self.Template_A00.Guess(trace)))
    b_B.append(self.Marginalizer.marginalize(self.Template_B00.Guess(trace)))
    b_A.append(self.Marginalizer.marginalize(self.Template_E01.Guess(trace), True))
    b_B.append(self.Marginalizer.marginalize(self.Template_B01.Guess(trace)))
    b_INP = self.in_table(pre_inputs)
    return b_INP, np.array(0.5*np.ones((2, 2, 320))), np.array(0.5*np.ones((2, 2, 320))), np.array(b_A), np.array(b_B)

def Table2State(Table):
  State = []
  for lane in range(0, 25):
    temp = 0
    for bit in range(0, 64):
      if Table[0][(lane*64+bit)]>0.5:
        temp ^= 0
      else:
        temp ^= (2**bit)
    State.append(temp)
  return State


def Consistent_Check(TableINP, TableA00):
  StateA00 = Table2State(TableA00)
  StateINP = Table2State(TableINP)
  temp0 = KEC.Back_RhoPi(StateA00)
  temp1 = KEC.Back_Theta(temp0)
  cal_stringH = KEC.lane2hex(temp1)
  inp_stringH = KEC.lane2hex(StateINP)
  Start = R_Size//4
  Next = KEC.Keccak_f1600(KEC.hex2lane(cal_stringH))
  if cal_stringH[Start:]==inp_stringH[Start:]:
    return True, temp1, Next
  else:
    return False, temp1, Next

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
    print('SHA3_input #'+str(tr).zfill(2))
    print('======================================================')
    rec_IN = ''
    prev = [0]*25
    Scan_it = [-1]*INVOC
    Suc_state = True
    for invoc in range(0, INVOC):
      trace = self.TRACE_FILES[invoc]['Traces'][tr][()]
      print('Template attack...')
      b_INP, b_C, b_D, b_A, b_B = self.TA.recovering(trace, prev)
      print('Loopy-BP processing...')
      INP, A_table, B_table, C_table, D_table, Scan_it[invoc] = SASCA_scan.State_Scan(2, b_INP, b_C, b_D, b_A, b_B)
      Suc, inv_in, inv_out = Consistent_Check(INP, A_table[0])
      Suc_state = Suc_state&Suc
      if Suc_state:
        print('Consistence check passed!')
        IN_XOR_bin = []
        for lane in range(0, 25):
          IN_XOR_bin.append(inv_in[lane]^prev[lane])
        IN_XOR_hex = KEC.lane2hex(IN_XOR_bin)
        rec_IN += (IN_XOR_hex[:(R_Size//4)])
        prev = inv_out
      else:
        print('Consistence check failed!')
        rec_IN = 'Not Found!'
        break 
    rec_IN = Keccak_input_strip(rec_IN)
    print(('Prediction: '+rec_IN))
    print(('Answer    : '+self.ans_inputs[tr]))
    pred_name = './Recovered_Data/recovered_inputs_'+str(tr).zfill(4)+'.npy'
    svm.Save(pred_name, rec_IN)
    iter_name = './Iterations/iteration_'+str(tr).zfill(4)+'.npy'
    svm.Save(iter_name, Scan_it)
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

