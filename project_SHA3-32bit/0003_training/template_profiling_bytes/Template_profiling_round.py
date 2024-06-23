import numpy as np
import time
import sys
import os
from numpy import linalg as LA
from sklearn.linear_model import LinearRegression
import serv_manager as svm
import h5py

Dir_iops = '../Code_find_IoPs/IoPs/'
Dir_intermediate = './intermediate_values/'
SET_NUM = 400
SET_SIZE = 160
Total_Tnum = SET_NUM*SET_SIZE

Bits = np.matrix(np.load('Bits.npy')[:,0:8])

def profiling_byte(tag, Re_Traces, byte):
  print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
  print(tag, 'byte: b'+str(byte).zfill(3))
  print('Loading Intermediate Values (in bits)...', time.asctime())
  intername = Dir_intermediate+'intermediate_B_'+tag+'/'+tag+'_b'+str(byte).zfill(3)+'.npy'
  InterBits = svm.Load(intername)
  ## LDA: Multiple Linear Regression ##################
  print(np.shape(Re_Traces))
  print('Linear regression...', time.asctime())
  reg = LinearRegression().fit(InterBits, Re_Traces)
  Expect = reg.predict(InterBits)
  ## LDA: W^{-1}*B ####################################
  print('Calculating       inter-class scatter B...', time.asctime())
  sub_inter = Expect-np.matrix(np.ones((Total_Tnum, 1)))*np.matrix(reg.predict(0.5*np.ones((1, 8))))
  Bmat = np.transpose(sub_inter)*sub_inter
  print('Calculating total intra-class scatter W...', time.asctime())
  sub_inner = np.matrix(Re_Traces)-Expect
  Wmat = np.transpose(sub_inner)*sub_inner
  ## LDA: Eigendecomposition ##########################
  print('Eigendecomposition...', time.asctime())
  AVectors = []
  Target = (Wmat.I)*Bmat
  EigVLs, EigVRs = LA.eig(Target)
  EigVLs = abs(EigVLs)
  tempEigVLs = EigVLs/sum(EigVLs)
  non_zero = 0
  for VIndx in range(0, len(tempEigVLs)):
    if tempEigVLs[VIndx]>0.00001:
      print(VIndx, tempEigVLs[VIndx])
      non_zero+=1
      AVectors.append(EigVRs[:,VIndx])
  AVectors = np.matrix(np.hstack(AVectors))
  print('There are '+str(non_zero)+' non-zero vectors')
  print('Total: ', sum(EigVLs))
  print('Compressing', time.asctime())
  Scov = np.transpose(AVectors)*Wmat*AVectors
  Scov *= 1.0/(float(Total_Tnum-9))
  #######################################################
  fname = './templateLDA_O010/template_'+tag+'/template'
  Sname = fname+'_scov_b'+str(byte).zfill(3)+'.npy'
  svm.Save(Sname, np.asarray(Scov))
  Aname = fname+'_avts_b'+str(byte).zfill(3)+'.npy'
  svm.Save(Aname, np.asarray(AVectors))
  Expects = reg.predict(Bits)*AVectors
  Ename = fname+'_expect_b'+str(byte).zfill(3)+'.npy'
  svm.Save(Ename, np.asarray(Expects))
  print('  Finished.', time.asctime())
  return

def profiling_word(tag, word):
  print('========================================================================')
  print(tag, 'word: i'+str(word).zfill(2))
  print('Loading resampled points of interests', time.asctime())
  fname = Dir_iops+'Ints_'+tag+'_i'+str(word).zfill(2)+'.hdf5'
  FILE = h5py.File(fname, 'r')  
  Re_Traces = FILE['IoPs'][()]
  FILE.close()
  for byte in range(4*word, 4*word+4):
    profiling_byte(tag, Re_Traces, byte)
  return

def profiling_state(tag, lower, upper):
  print('========================================================================')
  print('Profiling templates for '+tag)
  tS = time.time()
  print(time.asctime())
  for word in range(lower, upper):
    profiling_word(tag, word)
    print(time.asctime())
  tE = time.time()
  print('Exe. time = ', tE-tS)
  return

def profiling_round(RD):
  profiling_state(('A'+str(RD).zfill(2)), 0, 50)
  profiling_state(('B'+str(RD).zfill(2)), 0, 50)
  profiling_state(('C'+str(RD).zfill(2)), 0, 10)
  profiling_state(('D'+str(RD).zfill(2)), 0, 10)
  return

if __name__=='__main__':
  profiling_round(int(sys.argv[1]))


