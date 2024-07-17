import numpy as np
import os
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import serv_manager as svm
import time
import h5py

OUTSIZE = 36000
GROUPSIZE = 160
SETS = 100

class Scatter_Model:
  def __init__(self):
    print('Loading Samples...', time.asctime())
    fname = '../Peaks_HDF5/part_00.hdf5'
    print('Loading '+fname)
    FILE = h5py.File(fname, 'r')
    self.Samples = FILE['Traces'][()]
    FILE.close()
    print('Shape of trace samples:', np.shape(self.Samples), time.asctime())
    return
  
  def get_values(self, intermediate_bits):
    Expect = np.matrix(np.zeros(((GROUPSIZE*SETS), OUTSIZE)))
    print('Linear Regression ', time.asctime())
    reg = LinearRegression().fit(intermediate_bits, self.Samples)
    expect_byte = reg.predict(intermediate_bits)
    Scores = r2_score(self.Samples, expect_byte, multioutput='raw_values')
    print('Finished', time.asctime())
    return Scores

def detect(MODEL, TAG, lower, upper):
  for byte in range(lower, upper):
    print('================================================================')
    tS = time.time()
    BYTE_TAG = TAG+'_b'+str(byte).zfill(3)
    print(BYTE_TAG)
    intermediate_bits = svm.Load('intermediate_values/intermediate_B_'+TAG+'/'+BYTE_TAG+'.npy')[:(GROUPSIZE*SETS)]
    Scores = MODEL.get_values(intermediate_bits)
    fname = './detect_results_08/'+TAG+'_r_squ_b'+str(byte).zfill(3)+'.npy'
    svm.Save(fname, Scores)
    tE = time.time()
    print('Exe. time =', (tE-tS))
  return

if __name__=='__main__':
  model = Scatter_Model()
  detect(model, 'A00', 192, 194)
  detect(model, 'E01',   9,  11)

