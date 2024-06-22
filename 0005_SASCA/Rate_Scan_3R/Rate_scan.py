import numpy as np
import SASCA_scan
import serv_manager as svm
import os
import sys
import time

###################################################################################
# Independent parameters
# Rounds:
ROUND = 3
Dir_Table = 'Bit_Tables/'
###################################################################################

def get_prediction(Table):
  State = []
  for bit in range(0, 1600):
    if Table[0][bit]>0.5:
      State.append(0)
    else:
      State.append(1)
  return np.array(State)

def loopy_BP_scan(tr):
  print('======================================================')
  print('Trace: '+str(tr).zfill(4)+' '+time.asctime())
  #print('Table loading...')
  b_ALL = svm.Load((Dir_Table+'Tables_INP/table_'+str(tr).zfill(4)+'.npy'))
  b_C = []
  b_D = []
  b_A = []
  b_B = []
  for rd in range(0, ROUND):
    b_C.append(svm.Load((Dir_Table+'Tables_C'+str(rd).zfill(2)+'/table_'+str(tr).zfill(4)+'.npy')))
    b_D.append(svm.Load((Dir_Table+'Tables_D'+str(rd).zfill(2)+'/table_'+str(tr).zfill(4)+'.npy')))
    b_A.append(svm.Load((Dir_Table+'Tables_A'+str(rd).zfill(2)+'/table_'+str(tr).zfill(4)+'.npy')))
    b_B.append(svm.Load((Dir_Table+'Tables_B'+str(rd).zfill(2)+'/table_'+str(tr).zfill(4)+'.npy')))
  #print('Loading answer...')
  answer = svm.Load('answer_bit/answers_A00/ans_bit_'+str(tr).zfill(4)+'.npy')
  #print('Loopy-BP processing...')
  Results = []
  for byte in range(0, 201):
    #print('  ================================================')
    rate = byte*8
    b_INP = np.hstack([0.5*np.ones((2, rate)), b_ALL[:,rate:]])
    A00_table = SASCA_scan.State_Scan(ROUND, b_INP, np.array(b_C), np.array(b_D), np.array(b_A), np.array(b_B))
    prediction = get_prediction(A00_table)
    check = (np.count_nonzero(prediction==answer)==1600)
    #print('  rate '+str(rate).zfill(4)+':', check)
    Results.append(check)
  print('Saving results')
  svm.Save(('Success/success_'+str(tr).zfill(4)+'.npy'), Results)
  return

if __name__=='__main__':
  L = int(sys.argv[1])
  U = int(sys.argv[2])
  tS = time.time()
  for t in range(L, U):
    loopy_BP_scan(t)
  print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
  tE = time.time()
  print('Finished!')
  print('Exec. Time:', (tE-tS))


