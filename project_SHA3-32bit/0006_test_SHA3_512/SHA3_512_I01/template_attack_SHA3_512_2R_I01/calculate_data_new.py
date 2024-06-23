import numpy as np
import sys

def MAIN(L, U):
  Outlines = "& & Med. & Mean & $\\sigma$ & Max \\\\\n\\hline\n"
  Record = []
  Success = []
  for s in range(L, U):
    Suc = np.load("Success/success_"+str(s).zfill(4)+".npy")
    Iter = np.load("Iterations/iteration_"+str(s).zfill(4)+".npy") 
    if Suc==False:
      print("Not found #"+str(s).zfill(4))
    Success.append(Suc)
    for inv in range(0, len(Iter)):
      if (Iter[inv]<200)and(Iter[inv]>0):
        Record.append(Iter[inv])
  Outlines += (' & '+str(Success.count(True)))
  if len(Record)==0:
    Outlines += (' & N/A ')
    Outlines += (' & N/A ')
    Outlines += (' & N/A ')
    Outlines += (' & N/A ')
  else:
    Outlines += (' & '+'{:.3f}'.format(np.median(Record)))
    Outlines += (' & '+'{:.3f}'.format(np.mean(Record)))
    Outlines += (' & '+'{:.3f}'.format(np.std(Record)))
    Outlines += (' & '+'{:.3f}'.format(max(Record)))
  Outlines += "\\\\\n\\hline\n"
  print(Outlines)

if __name__=='__main__':
  MAIN(int(sys.argv[1]), int(sys.argv[2]))
