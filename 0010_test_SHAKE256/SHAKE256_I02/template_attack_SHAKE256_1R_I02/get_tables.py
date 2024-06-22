import numpy as np
import time
import sys
import os
import serv_manager as svm

PPC = 10

class Template:
  def __init__(self, func):
    if (func[0]=="A")or(func[0]=="B")or(func[0]=="C")or(func[0]=="D"):
      if (int(func[1:3])>=0)or(int(func[1:3])<24):
        label = "ics_original_010/ics_"+func+"_i"
      else:
        print(("Class init error: "+func))
        sys.exit()
    else:
       print(("Class init error: "+func))
       sys.exit()
    if (func[0]=="A")or(func[0]=="B"):
      self.Size = 50
    elif (func[0]=="C")or(func[0]=="D"):
      self.Size = 10
    self.name = func
    print(("Initializing "+self.name))
    self.ICs = []
    fname = "templateLDA_O010/template_"+func+"/template"
    self.INV = []
    self.EXP = []
    self.AVE = []
    for ints in range(0, self.Size):
      ics_name = label+str(ints).zfill(2)+".npy"
      ics_byte = svm.Load(ics_name)
      self.ICs.append(ics_byte)
    for byte in range(0, (4*self.Size)):
      Sname = fname+"_scov_b"+str(byte).zfill(3)+".npy"
      Scov = svm.Load(Sname)
      matS = np.matrix(Scov)
      ImatS = matS.I
      self.INV.append(ImatS)
      Aname = fname+"_avts_b"+str(byte).zfill(3)+".npy"
      Avecs = svm.Load(Aname)
      Amat = np.matrix(Avecs)
      self.AVE.append(Amat)
      Ename = fname+"_expect_b"+str(byte).zfill(3)+".npy"
      Tmeans = svm.Load(Ename)
      Emat = np.matrix(Tmeans)
      self.EXP.append(Emat)

  def Guess(self, Trace):
    #print(("Guessing "+self.name))
    Byte_Prob_Table = []
    for ints in range(0, self.Size):
      ips = []
      for ic in range(0, len(self.ICs[ints])):
        for p in range(0, PPC):
          indx = self.ICs[ints][ic]*PPC+p
          ips.append(Trace[indx])
      ips_mat = np.matrix(ips)
      for byte in range(4*ints, 4*ints+4):
        Xm = ips_mat*self.AVE[byte]
        ImatS = self.INV[byte]
        matX = np.matrix(np.ones((256, 1)))*Xm - self.EXP[byte]
        pos = np.exp(-0.5*abs(np.sum(np.array(matX*ImatS)*np.array(matX), axis=1)))
        pos = pos/sum(pos)
        Prob = np.transpose(np.vstack([np.arange(256.0), pos]))
        Byte_Prob_Table.append(Prob)
    return Byte_Prob_Table



