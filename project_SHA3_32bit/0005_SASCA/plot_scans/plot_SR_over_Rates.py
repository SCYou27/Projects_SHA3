import sys
import numpy as np
import matplotlib.pyplot as plt
Total = {'4':1000.0, '3':1000.0, '2':1000.0}
X_NUM = 8*np.array((range(0, 201)))
def get_data(rd):
  fname = '../Rate_Scan_'+str(rd)+'R/rate_scan_'+str(rd)+'R_B.npy'
  Y = 100.0*(np.load(fname)/Total[str(rd)])
  return X_NUM, Y

def plot(Interval, if_show=False):
  fig, pic = plt.subplots(1, figsize=(6,4.5))
  for R in Interval:
    X, Y = get_data(R)
    plt.plot(X, Y, label=(str(R)+' rounds'))
  pic.set_xlim([0,1600])
  pic.set_ylim([-0.5,100.5])
  pic.set_xlabel('#Rate (unknown) bits')
  pic.set_ylabel('%Recovered traces')
  pic.legend()
  plt.savefig('SuccessOverRate.pdf', bbox_inches='tight', pad_inches=0.1)
  if if_show==True:
    plt.show()
  return

if __name__=='__main__':
  IT = [4, 3, 2]
  try:
    plot(IT, bool(sys.argv[1]))
  except:
    plot(IT)
