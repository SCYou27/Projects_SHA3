import numpy as np
import sys
import os
def ICS_Detect(Dir, tag, bnd):
  if tag[0]=='A' or tag[0]=='B':
    Size = 50
  elif tag[0]=='C' or tag[0]=='D':
    Size = 10
  print("Tag = "+tag+", Bound = "+str(bnd))
  for N in range(0, Size):
    ics_name = Dir+"ics_"+tag+"_i"+str(N).zfill(2)+".npy"
    ICS = []
    name = "detect_results_32/"+tag+"_r_squ_i"+str(N).zfill(3)+".npy"
    T = np.load(name)
    Count = 0
    for t in range(0, 14500):
      if T[t]>bnd:
        Count+=1
        ICS.append(t)
    print("  Reg #"+str(N).zfill(2)+", Count = "+str(Count))
    np.save(ics_name, ICS)
  return

if __name__=='__main__':
  BND = float(sys.argv[1])
  dirname = "ics_original_"+str(int(BND*1000)).zfill(3)+"/"
  zipname = dirname[:-1]+".zip"
  os.system(("mkdir "+dirname))
  Group = ['A', 'B', 'C', 'D']
  for g in Group:
    for rd in range(0, 4):
      tag = g+str(rd).zfill(2)
      ICS_Detect(dirname, tag, BND)
  os.system(("zip -qq "+zipname+" -r "+dirname))
  os.system(("rm -r "+dirname))
