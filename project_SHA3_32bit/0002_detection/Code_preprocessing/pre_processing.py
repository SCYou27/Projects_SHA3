import numpy as np
import os
from array import array
import sys
import KECCAK as kec
import serv_manager as svm
import time
import h5py
trace_len = 7500000
OFFSET = 75000+455
PPC = 500
OUTSIZE = 14500
R_Bound = 0.980
NAME_REF = "../../0001_reference/Code_reference/ref_trace.npy"
def preprocessing(HDF5_name, InputDir):
  # IO data checking.
  Data_In = svm.Load((InputDir+"data_in.npy"))
  Data_Out = svm.Load((InputDir+"data_out.npy"))
  for t in range(0, 16):
    print("==================================================")
    print("Checking #"+str(t))
    A = Data_Out[t]
    B = kec.SHA3_512(Data_In[t])
    print(A)
    print(B)
    if A!=B:
      print("Error: wrong output.")
      return False
  # Copying IO data.
  cp_cmd_in = "cp "+InputDir+"data_in.npy "
  cp_cmd_in += "data_raw_in/"+InputDir[2:-1]+"_data_in.npy"
  svm.System(cp_cmd_in)
  cp_cmd_out = "cp "+InputDir+"data_out.npy "
  cp_cmd_out += "data_raw_out/"+InputDir[2:-1]+"_data_out.npy"
  svm.System(cp_cmd_out)
  # Processing traces.
  Proc_Traces = []
  Corrs = []
  CorrName = "Corrcoefs/"+InputDir[6:-1]+".npy"
  Ref_Trace = svm.Load(NAME_REF)
  for t in range(0, 16):
    for inv in range(0, 10):
      print("=============================================================")
      InputName = InputDir+"trace_"+str(t).zfill(4)+"_"+str(inv)+"_ch0.bin"
      print(InputName)
      Samples = []
      input_file = svm.Open(InputName, 'rb')
      float_array = array('d')
      float_array.frombytes(input_file.read())
      input_file.close()
      corr = np.corrcoef(float_array, Ref_Trace)[0][1]
      print(corr)
      if corr<R_Bound:
        print("R-sqaure problem.")
        return False
      Corrs.append(corr)
      for S in range(0, OUTSIZE):
        lower = OFFSET+S*PPC+20
        upper = lower+50
        sample = sum(float_array[lower:upper])
        Samples.append(sample)
      Proc_Traces.append(Samples)
  Proc_Traces = np.vstack(Proc_Traces)
  print("Data saving.")
  FILE = h5py.File(HDF5_name, 'w')
  FILE.create_dataset('Traces', np.shape(Proc_Traces), 'f8', compression="gzip", compression_opts=9, data=Proc_Traces)
  FILE.close()
  svm.Save(CorrName, Corrs)
  return True

if __name__=='__main__':
  L = int(sys.argv[1])
  U = int(sys.argv[2])
  for Set_n in range(L, U):
    tS = time.time()
    tag = "DN_"+str(Set_n).zfill(4)
    in_dir = "./Raw_"+tag+"/"
    in_zip = "../Raw/Raw_"+tag+".zip"
    svm.System(("unzip "+in_zip))
    hdf5_name = "../Processed_HDF5/Processed_"+tag+".hdf5"
    Suc = preprocessing(hdf5_name, in_dir)
    svm.System(("rm -r "+in_dir))
    tE = time.time()
    print(tE-tS)
