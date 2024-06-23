import numpy as np
import sys
import os
import time
import serv_manager as svm
import SASCA_XR
import prob_scan as Prob

it_n = 200

def State_Scan(RD, INPt, T_C, T_D, T_A, T_B):
  It_Record = 0
  SASCA = SASCA_XR.X_Rounds_SASCA(RD, INPt, T_C, T_D, T_A, T_B)
  INP_steady = 0.5*np.ones((2, 1600))
  C_steady = 0.5*np.ones((RD, 2, 320))
  D_steady = 0.5*np.ones((RD, 2, 320))
  A_steady = 0.5*np.ones((RD, 2, 1600))
  B_steady = 0.5*np.ones((RD, 2, 1600))
  HD = [0.0]*5
  for t in range(1, it_n+1):
    #print("Iteration #"+str(t))
    it_str = str(t).zfill(3)
    SASCA.R_renew()
    SASCA.Q_renew()
    #print "  Saving tables..."
    INP_table = SASCA.Zeta_out('INP')
    C_table = []
    D_table = []
    A_table = []
    B_table = []
    for rd in range(0, RD):
      rd_str = str(rd).zfill(2)
      C_table.append(SASCA.Zeta_out('C'+rd_str))
      D_table.append(SASCA.Zeta_out('D'+rd_str))
      A_table.append(SASCA.Zeta_out('A'+rd_str))
      B_table.append(SASCA.Zeta_out('B'+rd_str))
    C_table = np.array(C_table)
    D_table = np.array(D_table)
    A_table = np.array(A_table)
    B_table = np.array(B_table)
    HD[0] = np.sum(abs(INP_table-INP_steady))
    HD[1] = np.sum(abs(A_table-A_steady))
    HD[2] = np.sum(abs(B_table-B_steady))
    HD[3] = np.sum(abs(C_table-C_steady))
    HD[4] = np.sum(abs(D_table-D_steady))
    INP_steady = INP_table
    A_steady = A_table
    B_steady = B_table
    C_steady = C_table
    D_steady = D_table
    Summation = sum(HD)
    #print(str(t).zfill(3)+": "+str(Summation))
    if Summation==0:
      break
  print("#Iterations:", t)
  return INP_table, A_table, B_table, C_table, D_table, t



