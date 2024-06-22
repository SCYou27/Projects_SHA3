import numpy as np
import sys
import time
import serv_manager as svm

RC = [ '0000000000000001', '0000000000008082',\
       '800000000000808A', '8000000080008000',\
       '000000000000808B', '0000000080000001',\
       '8000000080008081', '8000000000008009',\
       '000000000000008A', '0000000000000088',\
       '0000000080008009', '000000008000000A',\
       '000000008000808B', '800000000000008B',\
       '8000000000008089', '8000000000008003',\
       '8000000000008002', '8000000000000080',\
       '000000000000800A', '800000008000000A',\
       '8000000080008081', '8000000000008080',\
       '0000000080000001', '8000000080008008']

hex2int = {'0': 0, '1': 1, '2': 2, '3': 3,\
           '4': 4, '5': 5, '6': 6, '7': 7,\
           '8': 8, '9': 9, 'a':10, 'b':11,\
           'c':12, 'd':13, 'e':14, 'f':15}

table_Z = np.array([[1.0, 0.0]])
table_O = np.array([[0.0, 1.0]])

####################################################
def find_table(h_str):
  Size = 4*len(h_str)
  int_t = 0
  for c in h_str:
    int_t <<= 4
    int_t += hex2int[c]
  Bin = bin(int_t)[2:].zfill(Size)
  Table = np.zeros((0, 2))
  for b in Bin:
    if b=='0':
      Table = np.vstack([table_Z, Table])
    else:
      Table = np.vstack([table_O, Table])
  return np.transpose(Table)

def Norm(ARRAY):
  with np.errstate(divide='ignore', invalid='ignore'):
    T = np.sum(ARRAY, axis=0)
    ARRAY/=np.vstack([T,T])
    ARRAY = np.nan_to_num(ARRAY, copy=True, nan=0.0, posinf=0.0, neginf=0.0)
  return ARRAY

class A_variable:
  def __init__(self, table=np.ones((2, 1600))):
    self.I0 = table
    self.Size = len(table[0])
    self.RT = np.ones((2, self.Size))
    self.RC = np.ones((2, self.Size))
    return
  
  def Output_Q(self):
    QT = self.RC*self.I0
    QC = self.RT*self.I0
    QT = np.hstack([QT[:,   0:  64], \
                    QT[:, 641: 704], QT[:, 640: 641], \
                    QT[:,1342:1344], QT[:,1280:1342], \
                    QT[:, 348: 384], QT[:, 320: 348], \
                    QT[:, 987:1024], QT[:, 960: 987], \
                    QT[:,1060:1088], QT[:,1024:1060], \
                    QT[:, 108: 128], QT[:,  64: 108], \
                    QT[:, 710: 768], QT[:, 704: 710], \
                    QT[:,1399:1408], QT[:,1344:1399], \
                    QT[:, 404: 448], QT[:, 384: 404], \
                    QT[:, 451: 512], QT[:, 448: 451], \
                    QT[:,1098:1152], QT[:,1088:1098], \
                    QT[:, 171: 192], QT[:, 128: 171], \
                    QT[:, 793: 832], QT[:, 768: 793], \
                    QT[:,1447:1472], QT[:,1408:1447], \
                    QT[:,1513:1536], QT[:,1472:1513], \
                    QT[:, 557: 576], QT[:, 512: 557], \
                    QT[:,1167:1216], QT[:,1152:1167], \
                    QT[:, 213: 256], QT[:, 192: 213], \
                    QT[:, 840: 896], QT[:, 832: 840], \
                    QT[:, 914: 960], QT[:, 896: 914], \
                    QT[:,1538:1600], QT[:,1536:1538], \
                    QT[:, 637: 640], QT[:, 576: 637], \
                    QT[:,1272:1280], QT[:,1216:1272], \
                    QT[:, 270: 320], QT[:, 256: 270]])
    return QT, QC
  
  def Renew_RT(self, R):
    R = Norm(R)
    self.RT = np.hstack([R[:,   0:  64], \
                         R[:, 404: 448], R[:, 384: 404], \
                         R[:, 789: 832], R[:, 768: 789], \
                         R[:,1195:1216], R[:,1152:1195], \
                         R[:,1586:1600], R[:,1536:1586], \
                         R[:, 228: 256], R[:, 192: 228], \
                         R[:, 620: 640], R[:, 576: 620], \
                         R[:, 701: 704], R[:, 640: 701], \
                         R[:,1043:1088], R[:,1024:1043], \
                         R[:,1411:1472], R[:,1408:1411], \
                         R[:, 127: 128], R[:,  64: 127], \
                         R[:, 506: 512], R[:, 448: 506], \
                         R[:, 871: 896], R[:, 832: 871], \
                         R[:,1272:1280], R[:,1216:1272], \
                         R[:,1326:1344], R[:,1280:1326], \
                         R[:, 293: 320], R[:, 256: 293], \
                         R[:, 348: 384], R[:, 320: 348], \
                         R[:, 758: 768], R[:, 704: 758], \
                         R[:,1137:1152], R[:,1088:1137], \
                         R[:,1480:1536], R[:,1472:1480], \
                         R[:, 130: 192], R[:, 128: 130], \
                         R[:, 521: 576], R[:, 512: 521], \
                         R[:, 921: 960], R[:, 896: 921], \
                         R[:, 983:1024], R[:, 960: 983], \
                         R[:,1406:1408], R[:,1344:1406]])
    return
  
  def Renew_RC(self, R):
    self.RC = Norm(R)
    return
  
  def Zeta(self):
    output = Norm(self.RT*self.RC*self.I0)
    return output

class B_variable:
  def __init__(self, table=np.ones((2, 1600)), RD=-1):
    self.RD = RD
    if (self.RD>-1)and(self.RD<24):
      self.S_Z = find_table(RC[self.RD].lower())
      self.S_O = np.ones((2, 64))-self.S_Z
    self.I0 = table
    self.Size = len(table[0])
    self.RC = np.ones((2, self.Size)) # To Chi
    self.RT = np.ones((2, self.Size)) # To Theta 3 (A)
    self.RF = np.ones((2, self.Size)) # To Theta 1 (C)
    return
  
  def Add_Constant(self, State):
    S_Z = np.sum((State[:,0:64]*self.S_Z), axis=0)
    S_O = np.sum((State[:,0:64]*self.S_O), axis=0)
    Lane = np.vstack([S_Z, S_O])
    return np.hstack([Lane, State[:,64:1600]])
  
  def Output_Q(self):
    QC = self.RT*self.RF*self.I0
    QT = self.RC*self.RF*self.I0
    QF = self.RC*self.RT*self.I0
    if self.RD==-1:
      return QC, QT, QF
    else:
      return QC, self.Add_Constant(QT), self.Add_Constant(QF)
  
  def Renew_RC(self, R):
    self.RC = Norm(R)
    return
  
  def Renew_RT(self, R):
    if self.RD==-1:
      self.RT = Norm(R)
    else:
      self.RT = self.Add_Constant(Norm(R))
    return
  
  def Renew_RF(self, R):
    if self.RD==-1:
      self.RF = Norm(R)
    else:
      self.RF = self.Add_Constant(Norm(R))
    return
  
  def Zeta(self):
    output = Norm(self.RC*self.RT*self.RF*self.I0)
    return output  

class C_variable:
  def __init__(self, table=np.ones((2, 320))):
    self.I0 = table
    self.Size = len(table[0])
    self.R0 = np.ones((2, self.Size)) #To the first Theta factor.
    self.R1 = np.ones((2, self.Size)) #To the second Theta factor in the same slice.
    self.R2 = np.ones((2, self.Size)) #To the second Theta factor in the latter slice.
    return
  
  def Output_Q(self):
    Q0 = self.R1*self.R2*self.I0
    Q1 = self.R0*self.R2*self.I0
    Q2 = self.R0*self.R1*self.I0
    return Q0, Q1, Q2
  
  def Renew_R0(self, R):
    self.R0 = Norm(R)
    return
  
  def Renew_R1(self, R):
    self.R1 = Norm(R)
    return
  
  def Renew_R2(self, R):
    self.R2 = Norm(R)
    return
  
  def Zeta(self):
    output = Norm(self.R0*self.R1*self.R2*self.I0)
    return output

class D_variable:
  def __init__(self, table=np.ones((2, 320))):
    self.I0 = table
    self.Size = len(table[0])
    self.R0 = np.ones((2, self.Size))
    self.R1 = np.ones((2, self.Size))
    self.R2 = np.ones((2, self.Size))
    self.R3 = np.ones((2, self.Size))
    self.R4 = np.ones((2, self.Size))
    self.RF = np.ones((2, self.Size)) #To the second Theta factor.
    return
  
  def Output_Q(self):
    Q0 = self.R1*self.R2*self.R3*self.R4*self.RF*self.I0
    Q1 = self.R0*self.R2*self.R3*self.R4*self.RF*self.I0
    Q2 = self.R0*self.R1*self.R3*self.R4*self.RF*self.I0
    Q3 = self.R0*self.R1*self.R2*self.R4*self.RF*self.I0
    Q4 = self.R0*self.R1*self.R2*self.R3*self.RF*self.I0
    QF = self.R0*self.R1*self.R2*self.R3*self.R4*self.I0
    return np.hstack([Q0, Q1, Q2, Q3, Q4]), QF
  
  def Renew_RN(self, R):
    R = Norm(R)
    self.R0 = R[:,   0: 320]
    self.R1 = R[:, 320: 640]
    self.R2 = R[:, 640: 960]
    self.R3 = R[:, 960:1280]
    self.R4 = R[:,1280:1600]
    return
  
  def Renew_RF(self, R):
    self.RF = Norm(R)
    return
  
  def Zeta(self):
    output = Norm(self.R0*self.R1*self.R2*self.R3*self.R4*self.RF*self.I0)
    return output


class THETA_factor_first:
  def __init__(self):
    self.Size = 320
    self.Q0 = np.ones((2, self.Size))
    self.Q1 = np.ones((2, self.Size))
    self.Q2 = np.ones((2, self.Size))
    self.Q3 = np.ones((2, self.Size))
    self.Q4 = np.ones((2, self.Size))
    self.QC = np.ones((2, self.Size)) #To the BC.
    return
  
  def Output_R(self):
    R0 = np.zeros((2, self.Size))
    R1 = np.zeros((2, self.Size))
    R2 = np.zeros((2, self.Size))
    R3 = np.zeros((2, self.Size))
    R4 = np.zeros((2, self.Size))
    RC = np.zeros((2, self.Size))
    for t0 in range(0, 2):
      for t1 in range(0, 2):
        for t2 in range(0, 2):
          for t3 in range(0, 2):
            for t4 in range(0, 2):
              tf = (t0^t1^t2^t3^t4)&0x1
              R0[t0] += self.Q1[t1]*self.Q2[t2]*self.Q3[t3]*self.Q4[t4]*self.QC[tf]
              R1[t1] += self.Q0[t0]*self.Q2[t2]*self.Q3[t3]*self.Q4[t4]*self.QC[tf]
              R2[t2] += self.Q0[t0]*self.Q1[t1]*self.Q3[t3]*self.Q4[t4]*self.QC[tf]
              R3[t3] += self.Q0[t0]*self.Q1[t1]*self.Q2[t2]*self.Q4[t4]*self.QC[tf]
              R4[t4] += self.Q0[t0]*self.Q1[t1]*self.Q2[t2]*self.Q3[t3]*self.QC[tf]
              RC[tf] += self.Q0[t0]*self.Q1[t1]*self.Q2[t2]*self.Q3[t3]*self.Q4[t4]
    return np.hstack([R0, R1, R2, R3, R4]), RC
  
  def Renew_QB(self, Q):
    Q = Norm(Q)
    self.Q0 = Q[:,   0: 320]
    self.Q1 = Q[:, 320: 640]
    self.Q2 = Q[:, 640: 960]
    self.Q3 = Q[:, 960:1280]
    self.Q4 = Q[:,1280:1600]
    return
  
  def Renew_QC(self, Q):
    self.QC = Norm(Q)
    return

class THETA_factor_second:
  def __init__(self):
    self.Size = 320
    self.Q0 = np.ones((2, self.Size)) #To the BC vector in the same slice.
    self.Q1 = np.ones((2, self.Size)) #To the BC vector in the previous slice.
    self.QD = np.ones((2, self.Size)) #To the BD vector.
    return
  
  def Output_R(self):
    R0 = np.zeros((2, self.Size))
    R1 = np.zeros((2, self.Size))
    RD = np.zeros((2, self.Size))
    for t0 in range(0, 2):
      for t1 in range(0, 2):
        td = (t0^t1)&0x1
        R0[t0] += self.Q1[t1]*self.QD[td]
        R1[t1] += self.Q0[t0]*self.QD[td]
        RD[td] += self.Q0[t0]*self.Q1[t1]
    R0 = np.hstack([R0[:, 64:320], R0[:,  0: 64]])
    R1 = np.hstack([R1[:,257:320], R1[:,256:257], \
                    R1[:,  1: 64], R1[:,  0:  1], \
                    R1[:, 65:128], R1[:, 64: 65], \
                    R1[:,129:192], R1[:,128:129], \
                    R1[:,193:256], R1[:,192:193]])
    return R0, R1, RD
  
  def Renew_Q0(self, Q0):
    self.Q0 = Norm(np.hstack([Q0[:,256:320], Q0[:,  0:256]]))
    return
  
  def Renew_Q1(self, Q1):
    self.Q1 = Norm(np.hstack([Q1[:,127:128], Q1[:, 64:127], \
                              Q1[:,191:192], Q1[:,128:191], \
                              Q1[:,255:256], Q1[:,192:255], \
                              Q1[:,319:320], Q1[:,256:319], \
                              Q1[:, 63: 64], Q1[:,  0: 63]]))
    return
  
  def Renew_QD(self, QD):
    self.QD = Norm(QD)
    return

class THETA_factor_third:
  def __init__(self):
    self.Size = 1600
    self.QD = np.ones((2, self.Size))
    self.QB = np.ones((2, self.Size))
    self.QA = np.ones((2, self.Size))
    return
  
  def Output_R(self):
    RD = np.zeros((2, self.Size))
    RB = np.zeros((2, self.Size))
    RA = np.zeros((2, self.Size))
    for td in range(0, 2):
      for tb in range(0, 2):
        ta = (td^tb)&0x1
        RD[td] += self.QB[tb]*self.QA[ta]
        RB[tb] += self.QD[td]*self.QA[ta]
        RA[ta] += self.QD[td]*self.QB[tb]
    return RD, RB, RA
  
  def Renew_QD(self, Q):
    self.QD = Norm(Q)
    return
  
  def Renew_QB(self, Q):
    self.QB = Norm(Q)
    return
  
  def Renew_QA(self, Q):
    self.QA = Norm(Q)
    return

class CHI_factor:
  def __init__(self):
    self.Size = 320
    self.QB0 = np.ones((2, self.Size))
    self.QB1 = np.ones((2, self.Size))
    self.QB2 = np.ones((2, self.Size))
    self.QB3 = np.ones((2, self.Size))
    self.QB4 = np.ones((2, self.Size))
    self.QA0 = np.ones((2, self.Size))
    self.QA1 = np.ones((2, self.Size))
    self.QA2 = np.ones((2, self.Size))
    self.QA3 = np.ones((2, self.Size))
    self.QA4 = np.ones((2, self.Size))
    return
  
  def constraint(self, x0, x1, x2, x3, x4):
    o0 = ((x0^((0x1^x1)&x2)))&0x1
    o1 = ((x1^((0x1^x2)&x3)))&0x1
    o2 = ((x2^((0x1^x3)&x4)))&0x1
    o3 = ((x3^((0x1^x4)&x0)))&0x1
    o4 = ((x4^((0x1^x0)&x1)))&0x1
    return o0, o1, o2, o3, o4
  
  def Output_R(self):
    RB0 = np.zeros((2, self.Size))
    RB1 = np.zeros((2, self.Size))
    RB2 = np.zeros((2, self.Size))
    RB3 = np.zeros((2, self.Size))
    RB4 = np.zeros((2, self.Size))
    RA0 = np.zeros((2, self.Size))
    RA1 = np.zeros((2, self.Size))
    RA2 = np.zeros((2, self.Size))
    RA3 = np.zeros((2, self.Size))
    RA4 = np.zeros((2, self.Size))
    for t0 in range(0, 2):
      for t1 in range(0, 2):
        for t2 in range(0, 2):
          for t3 in range(0, 2):
            for t4 in range(0, 2):
              z0, z1, z2, z3, z4 = self.constraint(t0, t1, t2, t3, t4)
              RB0[z0] += self.QA0[t0]*self.QA1[t1]*self.QA2[t2]*self.QA3[t3]*self.QA4[t4]*self.QB1[z1]*self.QB2[z2]*self.QB3[z3]*self.QB4[z4]
              RB1[z1] += self.QA0[t0]*self.QA1[t1]*self.QA2[t2]*self.QA3[t3]*self.QA4[t4]*self.QB0[z0]*self.QB2[z2]*self.QB3[z3]*self.QB4[z4]
              RB2[z2] += self.QA0[t0]*self.QA1[t1]*self.QA2[t2]*self.QA3[t3]*self.QA4[t4]*self.QB0[z0]*self.QB1[z1]*self.QB3[z3]*self.QB4[z4]
              RB3[z3] += self.QA0[t0]*self.QA1[t1]*self.QA2[t2]*self.QA3[t3]*self.QA4[t4]*self.QB0[z0]*self.QB1[z1]*self.QB2[z2]*self.QB4[z4]
              RB4[z4] += self.QA0[t0]*self.QA1[t1]*self.QA2[t2]*self.QA3[t3]*self.QA4[t4]*self.QB0[z0]*self.QB1[z1]*self.QB2[z2]*self.QB3[z3]
              RA0[t0] += self.QA1[t1]*self.QA2[t2]*self.QA3[t3]*self.QA4[t4]*self.QB0[z0]*self.QB1[z1]*self.QB2[z2]*self.QB3[z3]*self.QB4[z4]
              RA1[t1] += self.QA0[t0]*self.QA2[t2]*self.QA3[t3]*self.QA4[t4]*self.QB0[z0]*self.QB1[z1]*self.QB2[z2]*self.QB3[z3]*self.QB4[z4]
              RA2[t2] += self.QA0[t0]*self.QA1[t1]*self.QA3[t3]*self.QA4[t4]*self.QB0[z0]*self.QB1[z1]*self.QB2[z2]*self.QB3[z3]*self.QB4[z4]
              RA3[t3] += self.QA0[t0]*self.QA1[t1]*self.QA2[t2]*self.QA4[t4]*self.QB0[z0]*self.QB1[z1]*self.QB2[z2]*self.QB3[z3]*self.QB4[z4]
              RA4[t4] += self.QA0[t0]*self.QA1[t1]*self.QA2[t2]*self.QA3[t3]*self.QB0[z0]*self.QB1[z1]*self.QB2[z2]*self.QB3[z3]*self.QB4[z4]
    RB = np.hstack([RB0[:,  0: 64], RB1[:,  0: 64], RB2[:,  0: 64], RB3[:,  0: 64], RB4[:,  0: 64], \
                    RB0[:, 64:128], RB1[:, 64:128], RB2[:, 64:128], RB3[:, 64:128], RB4[:, 64:128], \
                    RB0[:,128:192], RB1[:,128:192], RB2[:,128:192], RB3[:,128:192], RB4[:,128:192], \
                    RB0[:,192:256], RB1[:,192:256], RB2[:,192:256], RB3[:,192:256], RB4[:,192:256], \
                    RB0[:,256:320], RB1[:,256:320], RB2[:,256:320], RB3[:,256:320], RB4[:,256:320]])
    RA = np.hstack([RA0[:,  0: 64], RA1[:,  0: 64], RA2[:,  0: 64], RA3[:,  0: 64], RA4[:,  0: 64], \
                    RA0[:, 64:128], RA1[:, 64:128], RA2[:, 64:128], RA3[:, 64:128], RA4[:, 64:128], \
                    RA0[:,128:192], RA1[:,128:192], RA2[:,128:192], RA3[:,128:192], RA4[:,128:192], \
                    RA0[:,192:256], RA1[:,192:256], RA2[:,192:256], RA3[:,192:256], RA4[:,192:256], \
                    RA0[:,256:320], RA1[:,256:320], RA2[:,256:320], RA3[:,256:320], RA4[:,256:320]])
    return RA, RB
  
  def Renew_QB(self, Q):
    Q = Norm(Q)
    self.QB0 = np.hstack([Q[:,   0:  64], Q[:, 320: 384], Q[:, 640: 704], Q[:, 960:1024], Q[:,1280:1344]])
    self.QB1 = np.hstack([Q[:,  64: 128], Q[:, 384: 448], Q[:, 704: 768], Q[:,1024:1088], Q[:,1344:1408]])
    self.QB2 = np.hstack([Q[:, 128: 192], Q[:, 448: 512], Q[:, 768: 832], Q[:,1088:1152], Q[:,1408:1472]])
    self.QB3 = np.hstack([Q[:, 192: 256], Q[:, 512: 576], Q[:, 832: 896], Q[:,1152:1216], Q[:,1472:1536]])
    self.QB4 = np.hstack([Q[:, 256: 320], Q[:, 576: 640], Q[:, 896: 960], Q[:,1216:1280], Q[:,1536:1600]])
    return
  
  def Renew_QA(self, Q):
    Q = Norm(Q)
    self.QA0 = np.hstack([Q[:,   0:  64], Q[:, 320: 384], Q[:, 640: 704], Q[:, 960:1024], Q[:,1280:1344]])
    self.QA1 = np.hstack([Q[:,  64: 128], Q[:, 384: 448], Q[:, 704: 768], Q[:,1024:1088], Q[:,1344:1408]])
    self.QA2 = np.hstack([Q[:, 128: 192], Q[:, 448: 512], Q[:, 768: 832], Q[:,1088:1152], Q[:,1408:1472]])
    self.QA3 = np.hstack([Q[:, 192: 256], Q[:, 512: 576], Q[:, 832: 896], Q[:,1152:1216], Q[:,1472:1536]])
    self.QA4 = np.hstack([Q[:, 256: 320], Q[:, 576: 640], Q[:, 896: 960], Q[:,1216:1280], Q[:,1536:1600]])
    return


class X_Rounds_SASCA:
  def __init__(self, rounds, T_IN, T_C, T_D, T_A, T_B):
    self.RD = rounds
    self.IN_V = B_variable(T_IN)
    # Round init:
    self.C_V = []
    self.D_V = []
    self.A_V = []
    self.B_V = []
    self.THETA_F1 = []
    self.THETA_F2 = []
    self.THETA_F3 = []
    self.CHI_F = []
    for rd in range(0, self.RD):
      self.C_V.append(C_variable(T_C[rd]))
      self.D_V.append(D_variable(T_D[rd]))
      self.A_V.append(A_variable(T_A[rd]))
      self.B_V.append(B_variable(T_B[rd], rd))
      self.THETA_F1.append(THETA_factor_first())
      self.THETA_F2.append(THETA_factor_second())
      self.THETA_F3.append(THETA_factor_third())
      self.CHI_F.append(CHI_factor())
    return
  
  def R_renew(self):
    #print "R_renew"
    for rd in range(0, self.RD):
      #THETA 1 outputs
      RB, RC = self.THETA_F1[rd].Output_R()
      if rd==0:
        self.IN_V.Renew_RF(RB)
      else:
        self.B_V[rd-1].Renew_RF(RB)
      self.C_V[rd].Renew_R0(RC)
      # THETA 2 outputs
      R0, R1, RD = self.THETA_F2[rd].Output_R()
      self.C_V[rd].Renew_R1(R0)
      self.C_V[rd].Renew_R2(R1)
      self.D_V[rd].Renew_RF(RD)
      # THETA 3 outputs
      RD, RB, RA = self.THETA_F3[rd].Output_R()
      if rd==0:
        self.IN_V.Renew_RT(RB)
      else:
        self.B_V[rd-1].Renew_RT(RB)
      self.A_V[rd].Renew_RT(RA)
      self.D_V[rd].Renew_RN(RD)
      #CHI outputs
      RA, RB = self.CHI_F[rd].Output_R()
      self.A_V[rd].Renew_RC(RA)
      self.B_V[rd].Renew_RC(RB)
    return
  
  def Q_renew(self):
    #print "Q_renew"
    _, QST, QSF = self.IN_V.Output_Q()
    for rd in range(0, self.RD):
      self.THETA_F1[rd].Renew_QB(QSF)
      self.THETA_F3[rd].Renew_QB(QST)
      #C outputs
      Q0, Q1, Q2 = self.C_V[rd].Output_Q()
      self.THETA_F1[rd].Renew_QC(Q0)
      self.THETA_F2[rd].Renew_Q0(Q1)
      self.THETA_F2[rd].Renew_Q1(Q2)
      #D outputs
      QN, QF = self.D_V[rd].Output_Q()
      self.THETA_F3[rd].Renew_QD(QN)
      self.THETA_F2[rd].Renew_QD(QF)
      #A outputs
      QT, QC = self.A_V[rd].Output_Q()
      self.THETA_F3[rd].Renew_QA(QT)
      self.CHI_F[rd].Renew_QA(QC)
      #B outputs
      QC, QST, QSF = self.B_V[rd].Output_Q()
      self.CHI_F[rd].Renew_QB(QC)
    return
  
  def Zeta_out(self, func):
    if func=='INP':
      return self.IN_V.Zeta()
    else:
      fc = func[0]
      rd = int(func[1:])
      if fc=='C':
        return self.C_V[rd].Zeta()
      elif fc=='D':
        return self.D_V[rd].Zeta()
      elif fc=='A':
        return self.A_V[rd].Zeta()
      elif fc=='B':
        return self.B_V[rd].Zeta()

