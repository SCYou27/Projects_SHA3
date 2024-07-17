import numpy as np
import time
import sys
import os
import serv_manager as svm

PPC = 25

class Template:
  def __init__(self, func):
    if (func[0]=="A")or(func[0]=="B")or(func[0]=="C")or(func[0]=="D")or(func[0]=="E"):
      if (int(func[1:3])>=0)or(int(func[1:3])<24):
        label = "ics_combined_090/ics_"+func+"_b"
      else:
        print(("Class init error: "+func))
        sys.exit()
    else:
       print(("Class init error: "+func))
       sys.exit()
    if (func[0]=="A")or(func[0]=="B")or(func[0]=="E"):
      self.Size = 200
    elif (func[0]=="C")or(func[0]=="D"):
      self.Size = 40
    self.name = func
    print(("Initializing "+self.name))
    self.ICs = []
    fname = "templateLDA_C090/template_"+func+"/template"
    self.INV = []
    self.EXP = []
    self.AVE = []
    for byte in range(0, self.Size):
      ## Loading indeces of interesting clock cycles
      ics_name = label+str(byte).zfill(3)+".npy"
      ics_byte = svm.Load(ics_name)
      self.ICs.append(ics_byte)
      ## Loading templates
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
    for byte in range(0, self.Size):
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
      pos = pos/sum(pos)
      Prob = np.transpose(np.vstack([np.arange(256.0), pos]))
      Byte_Prob_Table.append(Prob)
    return Byte_Prob_Table



