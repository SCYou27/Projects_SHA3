import numpy as np
import os
from array import array
import sys
import serv_manager as svm
trace_len = 7500000

def read_wave(input_name):
  print(input_name)
  input_file = svm.Open(input_name, 'rb')
  float_array = array('d')
  float_array.frombytes(input_file.read())
  input_file.close()
  if len(float_array)==trace_len:
    return float_array
  else:
    print("Error: length.")
    exit()

def ref_calculate():
  total = np.array([0.0]*trace_len)
  for Set_n in range(0, 10):
    tag = "RE_"+str(Set_n).zfill(4)
    in_dir = "./Raw_"+tag+"/"
    in_zip = "../Raw/Raw_"+tag+".zip"
    svm.System(("unzip "+in_zip))
    for t in range(0, 16):
      for inv in range(0, 10):
        print("=============================================================")
        InputName = in_dir+"trace_"+str(t).zfill(4)+"_"+str(inv)+"_ch0.bin"
        trace = read_wave(InputName)
        total += trace
    svm.System(("rm -vr "+in_dir))
  Average = total/1600.0
  svm.Save("ref_trace.npy", Average)


if __name__=='__main__':
  ref_calculate()
