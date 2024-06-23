import numpy as np
import matplotlib.pyplot as plt
import sys

def plot_32(tag, int_s, L, U):
  plt.figure(figsize=(10, 5))
  filename = "./detect_results_32/"+tag+"_r_squ_i"+str(int_s).zfill(3)+".npy"
  Rsq = np.load(filename)[L:U]
  plt.plot(Rsq, label="Sum")
  for b in range((4*int_s) , (4*int_s+4)):
    filename = "./detect_results_08/"+tag+"_r_squ_b"+str(b).zfill(3)+".npy"
    Rsq = np.load(filename)[L:U]
    plt.plot(Rsq, label=(tag+str(b)))
  plt.legend()
  plt.show()
  return

if __name__=='__main__':
  # python3 plot_detection.py KEY 0
  Tag = sys.argv[1]      # 'KEY'
  Ins = int(sys.argv[2]) # 0
  try:
    lower = int(sys.argv[3])
    upper = int(sys.argv[4])
  except:
    lower = 0
    upper = 900
  plot_32(Tag, Ins, lower, upper)

