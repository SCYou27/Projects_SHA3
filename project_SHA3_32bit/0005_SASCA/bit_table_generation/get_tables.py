import numpy as np
import time
import sys
import os
import serv_manager as svm
import marginalization
import h5py

PPC = 10

class Template:
  def __init__(self, func):
    self.Marginalizer = marginalization.Marginalization(8, False)
    if (func[0]=='A')or(func[0]=='B')or(func[0]=='C')or(func[0]=='D'):
      if (int(func[1:3])>=0)or(int(func[1:3])<24):
        label = 'ics_original_010/ics_'+func+'_i'
      else:
        print(('Class init error: '+func))
        sys.exit()
    else:
       print(('Class init error: '+func))
       sys.exit()
    if (func[0]=='A')or(func[0]=='B'):
      self.Size = 50
    elif (func[0]=='C')or(func[0]=='D'):
      self.Size = 10
    self.name = func
    print(('Initializing '+self.name))
    self.ICs = []
    fname = 'templateLDA_O010/template_'+func+'/template'
    self.INV = []
    self.EXP = []
    self.AVE = []
    for ints in range(0, self.Size):
      ics_name = label+str(ints).zfill(2)+'.npy'
      ics_byte = svm.Load(ics_name)
      self.ICs.append(ics_byte)
    for frag in range(0, (4*self.Size)):
      Sname = fname+'_scov_b'+str(frag).zfill(3)+'.npy'
      Scov = svm.Load(Sname)
      matS = np.matrix(Scov)
      ImatS = matS.I
      self.INV.append(ImatS)
      Aname = fname+'_avts_b'+str(frag).zfill(3)+'.npy'
      Avecs = svm.Load(Aname)
      Amat = np.matrix(Avecs)
      self.AVE.append(Amat)
      Ename = fname+'_expect_b'+str(frag).zfill(3)+'.npy'
      Tmeans = svm.Load(Ename)
      Emat = np.matrix(Tmeans)
      self.EXP.append(Emat)

  def Guess(self, Trace):
    #print(('Guessing '+self.name))
    Frag_Prob_Table = []
    for ints in range(0, self.Size):
      ips = []
      for ic in range(0, len(self.ICs[ints])):
        for p in range(0, PPC):
          indx = self.ICs[ints][ic]*PPC+p
          ips.append(Trace[indx])
      ips_mat = np.matrix(ips)
      for frag in range(4*ints, 4*ints+4):
        Xm = ips_mat*self.AVE[frag]
        ImatS = self.INV[frag]
        matX = np.matrix(np.ones((256, 1)))*Xm - self.EXP[frag]
        pos = np.exp(-0.5*abs(np.sum(np.array(matX*ImatS)*np.array(matX), axis=1)))
        pos = pos/sum(pos)
        Prob = np.transpose(np.vstack([np.arange(256.0), pos]))
        Frag_Prob_Table.append(Prob)
    return self.Marginalizer.marginalize(np.array(Frag_Prob_Table))

def answer_to_table(answer_bits):
  table_O = 1.0*answer_bits
  return np.vstack([(1.0-table_O), table_O])

def main(L, U):
  Template_A00 = Template('A00')
  Template_A01 = Template('A01')
  Template_A02 = Template('A02')
  Template_A03 = Template('A03')
  Template_B00 = Template('B00')
  Template_B01 = Template('B01')
  Template_B02 = Template('B02')
  Template_B03 = Template('B03')
  Template_C00 = Template('C00')
  Template_C01 = Template('C01')
  Template_C02 = Template('C02')
  Template_C03 = Template('C03')
  Template_D00 = Template('D00')
  Template_D01 = Template('D01')
  Template_D02 = Template('D02')
  Template_D03 = Template('D03')
  print('Loading traces...')
  FILE = h5py.File('../../0004_validation/Processed_HDF5/part_00.hdf5', 'r')
  Traces = FILE['Traces'][()]
  FILE.close()
  output_head = 'Bit_Tables/Tables_'
  for tr in range(L, U):
    print('====================================================')
    print(time.asctime())
    print(('trace index: '+str(tr).zfill(4)), time.asctime())
    trace = Traces[tr]
    INP_name = 'answer_bit/answers_INP/ans_bit_'+str(tr).zfill(4)+'.npy'
    Table_INP = answer_to_table(svm.Load(INP_name))
    Guess_A00 = Template_A00.Guess(trace)
    Guess_A01 = Template_A01.Guess(trace)
    Guess_A02 = Template_A02.Guess(trace)
    Guess_A03 = Template_A03.Guess(trace)
    Guess_B00 = Template_B00.Guess(trace)
    Guess_B01 = Template_B01.Guess(trace)
    Guess_B02 = Template_B02.Guess(trace)
    Guess_B03 = Template_B03.Guess(trace)
    Guess_C00 = Template_C00.Guess(trace)
    Guess_C01 = Template_C01.Guess(trace)
    Guess_C02 = Template_C02.Guess(trace)
    Guess_C03 = Template_C03.Guess(trace)
    Guess_D00 = Template_D00.Guess(trace)
    Guess_D01 = Template_D01.Guess(trace)
    Guess_D02 = Template_D02.Guess(trace)
    Guess_D03 = Template_D03.Guess(trace)
    output_tail = 'table_'+str(tr).zfill(4)+'.npy'
    svm.Save((output_head+'INP/'+output_tail), Table_INP)
    svm.Save((output_head+'A00/'+output_tail), Guess_A00)
    svm.Save((output_head+'A01/'+output_tail), Guess_A01)
    svm.Save((output_head+'A02/'+output_tail), Guess_A02)
    svm.Save((output_head+'A03/'+output_tail), Guess_A03)
    svm.Save((output_head+'B00/'+output_tail), Guess_B00)
    svm.Save((output_head+'B01/'+output_tail), Guess_B01)
    svm.Save((output_head+'B02/'+output_tail), Guess_B02)
    svm.Save((output_head+'B03/'+output_tail), Guess_B03)
    svm.Save((output_head+'C00/'+output_tail), Guess_C00)
    svm.Save((output_head+'C01/'+output_tail), Guess_C01)
    svm.Save((output_head+'C02/'+output_tail), Guess_C02)
    svm.Save((output_head+'C03/'+output_tail), Guess_C03)
    svm.Save((output_head+'D00/'+output_tail), Guess_D00)
    svm.Save((output_head+'D01/'+output_tail), Guess_D01)
    svm.Save((output_head+'D02/'+output_tail), Guess_D02)
    svm.Save((output_head+'D03/'+output_tail), Guess_D03)
  return

if __name__=='__main__':
  lower = int(sys.argv[1])
  upper = int(sys.argv[2])
  main(lower, upper)
  print('==========================================')
  print('Finished!')
  print(time.asctime())

