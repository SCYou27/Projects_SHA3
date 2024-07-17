import numpy as np
import time
import sys
import os
import serv_manager as svm
import h5py

PPC = 25
TEST_SIZE = 1000
ICS_TAG = '090'
DIR_TEMPLATES = 'templateLDA_C'+ICS_TAG+'/'
DIR_ICS = 'ics_combined_'+ICS_TAG+'/'
DIR_TRACES = '../Processed_HDF5/'

def sortPos(val):
  return val[1]

class Template:
  def __init__(self, func):
    if (func[0]=='A')or(func[0]=='B')or(func[0]=='C')or(func[0]=='D')or(func[0]=='E'):
      if (int(func[1:3])>=0)or(int(func[1:3])<24):
        label = DIR_ICS+'ics_'+func+'_b'
      else:
        print(('Class init error: '+func))
        sys.exit()
    else:
       print(('Class init error: '+func))
       sys.exit()
    if (func[0]=='A')or(func[0]=='B')or(func[0]=='E'):
      self.Size = 200
    elif (func[0]=='C')or(func[0]=='D'):
      self.Size = 40
    self.name = func
    print(('Initializing '+self.name))
    self.ICs = []
    fname = DIR_TEMPLATES+'template_'+func+'/template'
    self.INV = []
    self.EXP = []
    self.AVE = []
    for byte in range(0, self.Size):
      ics_name = label+str(byte).zfill(3)+'.npy'
      ics_byte = svm.Load(ics_name)
      self.ICs.append(ics_byte)
      Sname = fname+'_scov_b'+str(byte).zfill(3)+'.npy'
      Scov = svm.Load(Sname)
      matS = np.matrix(Scov)
      ImatS = matS.I
      self.INV.append(ImatS)
      Aname = fname+'_avts_b'+str(byte).zfill(3)+'.npy'
      Avecs = svm.Load(Aname)
      Amat = np.matrix(Avecs)
      self.AVE.append(Amat)
      Ename = fname+'_expect_b'+str(byte).zfill(3)+'.npy'
      Tmeans = np.load(Ename)
      Emat = np.matrix(Tmeans)
      self.EXP.append(Emat)

  def Guess(self, Trace, ANSWERs, sortbyprob=False):
    print(('Guessing '+self.name))
    Rank_Table = []
    for byte in range(0, self.Size):
      #print 'Byte:', byte
      Poss = []
      ips = []
      for ic in range(0, len(self.ICs[byte])):
        for p in range(0, PPC):
          indx = self.ICs[byte][ic]*PPC+p
          ips.append(Trace[indx])
      ips_mat = np.matrix(ips)
      Xm = ips_mat*self.AVE[byte]
      ImatS = self.INV[byte]
      matX = np.matrix(np.ones((256, 1)))*Xm - self.EXP[byte]
      pos = np.exp(-0.5*abs(np.sum(np.array(matX*ImatS)*np.array(matX), axis=1)))
      for x in range(0, 256):
        tempPoss = []
        tempPoss.append(x)
        tempPoss.append(pos[x])
        Poss.append(tempPoss)
      if sortbyprob:
        Poss.sort(reverse=True, key = sortPos)
      for x in range(0, 256):
        if Poss[x][0]==ANSWERs[byte]:
          Rank_Table.append(x)
    return np.array(Rank_Table)

def main(set_n, trace_number=TEST_SIZE):
  Rank_A00 = np.zeros((trace_number, 200))
  Rank_B00 = np.zeros((trace_number, 200))
  Rank_E01 = np.zeros((trace_number, 200))
  Rank_B01 = np.zeros((trace_number, 200))
  print('Loading Answers...')
  temp_A00 = []
  temp_B00 = []
  temp_E01 = []
  temp_B01 = []
  Name_A00 = 'intermediate_values/intermediate_B_A00/A00_b'
  Name_B00 = 'intermediate_values/intermediate_B_B00/B00_b'
  Name_E01 = 'intermediate_values/intermediate_B_E01/E01_b'
  Name_B01 = 'intermediate_values/intermediate_B_B01/B01_b'
  for byte in range(0, 200):
    temp_A00.append(svm.Load((Name_A00+str(byte).zfill(3)+'.npy')))
    temp_B00.append(svm.Load((Name_B00+str(byte).zfill(3)+'.npy')))
    temp_E01.append(svm.Load((Name_E01+str(byte).zfill(3)+'.npy')))
    temp_B01.append(svm.Load((Name_B01+str(byte).zfill(3)+'.npy')))
  ANS_A00 = np.transpose(np.vstack(temp_A00))[(set_n*TEST_SIZE):(set_n*TEST_SIZE+trace_number),:]
  ANS_B00 = np.transpose(np.vstack(temp_B00))[(set_n*TEST_SIZE):(set_n*TEST_SIZE+trace_number),:]
  ANS_E01 = np.transpose(np.vstack(temp_E01))[(set_n*TEST_SIZE):(set_n*TEST_SIZE+trace_number),:]
  ANS_B01 = np.transpose(np.vstack(temp_B01))[(set_n*TEST_SIZE):(set_n*TEST_SIZE+trace_number),:]
  Template_A00 = Template('A00')
  Template_B00 = Template('B00')
  Template_E01 = Template('E01')
  Template_B01 = Template('B01')
  print('Loading Downsampled Traces...')
  FILE = h5py.File((DIR_TRACES+'part_'+str(set_n).zfill(2)+'.hdf5'), 'r')
  Traces = FILE['Traces'][()]
  FILE.close()
  for tr in range(0, trace_number):
    print('====================================================')
    print(time.asctime())
    print(('trace index: '+str(TEST_SIZE*set_n+tr).zfill(4)))
    trace = Traces[tr]
    Rank_A00[tr] = Template_A00.Guess(trace, ANS_A00[tr], True)
    Rank_B00[tr] = Template_B00.Guess(trace, ANS_B00[tr], True)
    Rank_E01[tr] = Template_E01.Guess(trace, ANS_E01[tr], True)
    Rank_B01[tr] = Template_B01.Guess(trace, ANS_B01[tr], True)
  for byte in range(0, 200):
    tail = str(byte).zfill(3)+'_s'+str(set_n).zfill(3)+'.npy'
    svm.Save(('./Rank_C'+ICS_TAG+'/rank_A00_b'+tail), Rank_A00[:,byte])
    svm.Save(('./Rank_C'+ICS_TAG+'/rank_B00_b'+tail), Rank_B00[:,byte])
    svm.Save(('./Rank_C'+ICS_TAG+'/rank_E01_b'+tail), Rank_E01[:,byte])
    svm.Save(('./Rank_C'+ICS_TAG+'/rank_B01_b'+tail), Rank_B01[:,byte])
  return

if __name__=='__main__':
  Set_n = 1
  TN = 10
  main(Set_n, TN)
  print('==========================================')
  print('Finished!')
  print(time.asctime())



