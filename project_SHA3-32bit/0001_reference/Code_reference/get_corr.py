import numpy as np
import os
from array import array
import sys
trace_len = 7500000

def read_wave(input_name):
  print(input_name)
  input_file = open(input_name, 'rb')
  float_array = array('d')
  float_array.frombytes(input_file.read())
  input_file.close()
  if len(float_array)==trace_len:
    return float_array
  else:
    print("Error: length.")
    exit()

def corr_calculate(set_size, set_num):
  trace_ref = np.load("ref_trace.npy")
  Corrs = []
  for Num in range(0, set_num):
    tag = "RE_"+str(Num).zfill(4)
    tr_dir = "./Raw_"+tag+"/"
    tr_zip = "../Raw/Raw_"+tag+".zip"
    os.system(("unzip "+tr_zip))
    for t in range(0, set_size):
      print("================================================")
      tr_name = tr_dir+"trace_"+str((t//10)).zfill(4)+"_"+str((t%10))+"_ch0.bin"
      trace = read_wave(tr_name)
      corr = np.corrcoef(trace, trace_ref)[0][1]
      Corrs.append(corr)
      print(corr)
    os.system(("rm -vr "+tr_dir))
  np.save("corrcoef.npy", Corrs)
  return

def show_statistics(set_size, set_num, Times):
  total_size = set_size*set_num
  Corrs = np.load("corrcoef.npy")
  Mean = np.mean(Corrs)
  Std = np.std(Corrs)
  print("=================================================================")
  print("Trace Number      : "+str(Mean))
  print("Standard deviation: "+str(Std))
  L_bound = Mean-Times*Std
  U_bound = Mean+Times*Std
  print("Interval ("+str(Times)+"x): ["+str(L_bound)+", "+str(U_bound)+"]")
  print("=================================================================")
  print("Non-qualified traces:")
  for t in range(0, total_size):
    if (Corrs[t]<L_bound) or (Corrs[t]>U_bound):
        print("Index: "+str(t).zfill(4)+", Corrcoef: "+str(Corrs[t]))
  return

if __name__=='__main__':
  Tag = sys.argv[1]
  Ts = int(sys.argv[2])
  S_size = 160
  S_num = 10
  if (Tag=="find") or (Tag=="all"):
    corr_calculate(S_size, S_num)
  if (Tag=="show") or (Tag=="all"):
    show_statistics(S_size, S_num, Ts)
