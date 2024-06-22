import numpy as np
import sys
import os
import time
import serv_manager as svm
import SASCA_XR

it_n = 40

def get_prediction(Table):
  State = np.zeros((1600), dtype=np.int32)
  for bit in range(0, 1600):
    if Table[0][bit]<=Table[1][bit]:
      State[bit] = 1
  return State


def State_Scan(RD, INPt, T_C, T_D, T_A, T_B):
  SASCA = SASCA_XR.X_Rounds_SASCA(RD, INPt, T_C, T_D, T_A, T_B)
  Predictions = []
  Predictions.append(get_prediction(SASCA.Zeta_out('A00')))
  for t in range(1, it_n+1):
    print("Iteration #"+str(t))
    SASCA.R_renew()
    SASCA.Q_renew()
    #print "  Saving tables..."
    Predictions.append(get_prediction(SASCA.Zeta_out('A00')))
  return np.array(Predictions)



