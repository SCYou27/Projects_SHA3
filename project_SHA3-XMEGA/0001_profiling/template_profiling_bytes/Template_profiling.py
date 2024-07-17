import numpy as np
import time
import sys
import os
from numpy import linalg as LA
from sklearn.linear_model import LinearRegression
import serv_manager as svm
import h5py
import get_IoPs

Dir_intermediate = './intermediate_values/'
SET_NUM = 200
SET_SIZE = 160
Total_Tnum = SET_NUM*SET_SIZE

Bits = np.matrix(np.load('Bits.npy')[:,0:8])

class Profiler:
  def __init__(self):
    self.Extractor = get_IoPs.IOPS_Extractor()
    return
  
  def close(self):
    self.Extractor.close()
    return
  
  def profiling_byte(self, tag, byte):
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print(tag, 'byte: b'+str(byte).zfill(3))
    ## Loading intermediate values
    print('Loading intermediate values (in bits)...', time.asctime())
    intername = Dir_intermediate+'intermediate_B_'+tag+'/'+tag+'_b'+str(byte).zfill(3)+'.npy'
    InterBits = svm.Load(intername)
    ## Loading points of interest
    print('Loading points of interest...', time.asctime())
    Re_Traces = self.Extractor.get_IoPs(tag, byte)
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
    fname = './templateLDA_C090/template_'+tag+'/template'
    Sname = fname+'_scov_b'+str(byte).zfill(3)+'.npy'
    svm.Save(Sname, np.asarray(Scov))
    Aname = fname+'_avts_b'+str(byte).zfill(3)+'.npy'
    svm.Save(Aname, np.asarray(AVectors))
    Expects = reg.predict(Bits)*AVectors
    Ename = fname+'_expect_b'+str(byte).zfill(3)+'.npy'
    svm.Save(Ename, np.asarray(Expects))
    print('  Finished.', time.asctime())
    return
  
  def profiling_state(self, tag, lower, upper):
    print('========================================================================')
    print('Profiling templates for '+tag)
    tS = time.time()
    print(time.asctime())
    for byte in range(lower, upper):
      self.profiling_byte(tag, byte)
      print(time.asctime())
    tE = time.time()
    print('Exe. time = ', tE-tS)
    return

if __name__=='__main__':
  Builder = Profiler()
  Builder.profiling_state('A00', 0, 2)
  Builder.profiling_state('B00', 2, 4)
  Builder.profiling_state('E01', 4, 6)
  Builder.profiling_state('B01', 6, 8)
  Builder.close()


