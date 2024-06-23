import numpy as np
import time
import sys
import os
import serv_manager as svm
import h5py

PPC = 10
TEST_SIZE = 1000
ICS_TAG = '010'
DIR_TEMPLATES = 'templateLDA_O'+ICS_TAG+'/'
DIR_ICS = 'ics_original_'+ICS_TAG+'/'
DIR_TRACES = '../Processed_HDF5/'

def sortPos(val):
  return val[1]

class Template:
  def __init__(self, func):
    if (func[0]=='A')or(func[0]=='B')or(func[0]=='C')or(func[0]=='D'):
      if (int(func[1:3])>=0)or(int(func[1:3])<24):
        label = DIR_ICS+'ics_'+func+'_i'
      else:
        print(('Class init error: '+func))
        sys.exit()
    else:
       print(('Class init error: '+func))
       sys.exit()
    if (func[0]=='A')or(func[0]=='B'):
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
      ints = byte//4
      ics_name = label+str(ints).zfill(2)+'.npy'
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
  Rank_A = np.zeros((4, trace_number, 200))
  Rank_B = np.zeros((4, trace_number, 200))
  Rank_C = np.zeros((4, trace_number,  40))
  Rank_D = np.zeros((4, trace_number,  40))
  ANS_A = np.zeros((4, trace_number, 200))
  ANS_B = np.zeros((4, trace_number, 200))
  ANS_C = np.zeros((4, trace_number,  40))
  ANS_D = np.zeros((4, trace_number,  40))
  Template_A = []
  Template_B = []
  Template_C = []
  Template_D = []
  print('Loading Answers...')
  for rd in range(0, 4):
    rd_tag = str(rd).zfill(2)
    temp_A = []
    temp_B = []
    temp_C = []
    temp_D = []
    Name_A = 'intermediate_values/intermediate_B_A'+rd_tag+'/A'+rd_tag+'_b'
    Name_B = 'intermediate_values/intermediate_B_B'+rd_tag+'/B'+rd_tag+'_b'
    Name_C = 'intermediate_values/intermediate_B_C'+rd_tag+'/C'+rd_tag+'_b'
    Name_D = 'intermediate_values/intermediate_B_D'+rd_tag+'/D'+rd_tag+'_b'
    for byte in range(0, 200):
      temp_A.append(svm.Load((Name_A+str(byte).zfill(3)+'.npy')))
      temp_B.append(svm.Load((Name_B+str(byte).zfill(3)+'.npy')))
      if byte>=40:
        continue
      temp_C.append(svm.Load((Name_C+str(byte).zfill(3)+'.npy')))
      temp_D.append(svm.Load((Name_D+str(byte).zfill(3)+'.npy')))
    ANS_A[rd] = np.transpose(np.vstack(temp_A))[(set_n*TEST_SIZE):(set_n*TEST_SIZE+trace_number),:]
    ANS_B[rd] = np.transpose(np.vstack(temp_B))[(set_n*TEST_SIZE):(set_n*TEST_SIZE+trace_number),:]
    ANS_C[rd] = np.transpose(np.vstack(temp_C))[(set_n*TEST_SIZE):(set_n*TEST_SIZE+trace_number),:]
    ANS_D[rd] = np.transpose(np.vstack(temp_D))[(set_n*TEST_SIZE):(set_n*TEST_SIZE+trace_number),:]
    Template_A.append(Template(('A'+rd_tag)))
    Template_B.append(Template(('B'+rd_tag)))
    Template_C.append(Template(('C'+rd_tag)))
    Template_D.append(Template(('D'+rd_tag)))
  print('Loading Downsampled Traces...')
  FILE = h5py.File((DIR_TRACES+'part_'+str(set_n).zfill(2)+'.hdf5'), 'r')
  Traces = FILE['Traces'][()]
  FILE.close()
  for tr in range(0, trace_number):
    print('====================================================')
    print(time.asctime())
    print(('trace index: '+str(TEST_SIZE*set_n+tr).zfill(4)))
    trace = Traces[tr]
    for rd in range(0, 4):
      Rank_A[rd][tr] = Template_A[rd].Guess(trace, ANS_A[rd][tr], True)
      Rank_B[rd][tr] = Template_B[rd].Guess(trace, ANS_B[rd][tr], True)
      Rank_C[rd][tr] = Template_C[rd].Guess(trace, ANS_C[rd][tr], True)
      Rank_D[rd][tr] = Template_D[rd].Guess(trace, ANS_D[rd][tr], True)
  for rd in range(0, 4):
    print('Saving Files (round '+str(rd)+')')
    for byte in range(0, 200):
      tail = str(rd).zfill(2)+'_b'+str(byte).zfill(3)+'_s'+str(set_n).zfill(3)+'.npy'
      svm.Save(('./Rank_O'+ICS_TAG+'/rank_A'+tail), Rank_A[rd][:,byte])
      svm.Save(('./Rank_O'+ICS_TAG+'/rank_B'+tail), Rank_B[rd][:,byte])
      if byte>=40:
        continue
      svm.Save(('./Rank_O'+ICS_TAG+'/rank_C'+tail), Rank_C[rd][:,byte])
      svm.Save(('./Rank_O'+ICS_TAG+'/rank_D'+tail), Rank_D[rd][:,byte])
  return

if __name__=='__main__':
  Set_n = 3
  TN = 10
  main(Set_n, TN)
  print('==========================================')
  print('Finished!')
  print(time.asctime())



