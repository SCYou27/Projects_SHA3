import numpy as np
import os
import sys
import combining_keys
KEY_F = combining_keys.forward()
KEY_B = combining_keys.backward()

def combine(TAG):
  OldZip = 'ics_original_'+TAG+'.zip'
  OldDir = 'ics_original_'+TAG+'/'
  NewZip = 'ics_combined_'+TAG+'.zip'
  NewDir = 'ics_combined_'+TAG+'/'
  os.system(('unzip '+OldZip))
  os.system(('mkdir '+NewDir))
  os.system(('cp '+OldDir+'ics_B*.npy '+NewDir))
  for rd in range(0, 2):
    Old_A = []
    Old_E = []
    # Load old files...
    for byte in range(0, 200):
      Old_A.append(np.load((OldDir+'ics_A'+str(rd).zfill(2)+'_b'+str(byte).zfill(3)+'.npy')))
      Old_E.append(np.load((OldDir+'ics_E'+str(rd).zfill(2)+'_b'+str(byte).zfill(3)+'.npy')))
    # Forward...
    for byte in range(0, 200):
      New_A = np.union1d(Old_A[byte], [])
      for t in range(0, len(KEY_F[byte])):
        New_A = np.union1d(New_A, Old_E[(KEY_F[byte][t])])
      np.save((NewDir+'ics_A'+str(rd).zfill(2)+'_b'+str(byte).zfill(3)+'.npy'), New_A.astype(int))
    # Backward...
    for byte in range(0, 200):
      New_E = np.union1d(Old_E[byte], [])
      for t in range(0, len(KEY_B[byte])):
        New_E = np.union1d(New_E, Old_A[(KEY_B[byte][t])])
      np.save((NewDir+'ics_E'+str(rd).zfill(2)+'_b'+str(byte).zfill(3)+'.npy'), New_E.astype(int))
  os.system(('zip '+NewZip+' -r '+NewDir))
  os.system(('rm -r '+NewDir))
  os.system(('rm -r '+OldDir))
  return

if __name__=='__main__':
  tag = sys.argv[1]
  combine(tag)
