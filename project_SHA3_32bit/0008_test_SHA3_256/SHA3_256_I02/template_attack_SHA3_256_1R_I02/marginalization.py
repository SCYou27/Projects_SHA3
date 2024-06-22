import numpy as np
class Marginalization:
  def __init__(self, bit_size, ver = False):
    tmp = np.arange((2**bit_size))
    self.Bits_O = np.zeros((0, 2**bit_size))
    for t in range(0, bit_size):
      mask = 2**t
      self.Bits_O = np.vstack([self.Bits_O, (mask&tmp)//mask])
    self.Bits_O = np.matrix(self.Bits_O)
    self.Bits_Z = np.matrix(np.ones((bit_size, 2**bit_size)))-self.Bits_O
    if ver:
      print(self.Bits_O)
      print(self.Bits_Z)
    return
  
  def marginalize(self, Prob_Table):
    BitTable = np.zeros((0, 2))
    for frag in range(0, len(Prob_Table)):
      Prob = np.matrix(Prob_Table[frag])[:,1]
      Prob_marginal = np.hstack([(self.Bits_Z*Prob), (self.Bits_O*Prob)])
      BitTable = np.vstack([BitTable, Prob_marginal])
    return np.transpose(BitTable)

if __name__=='__main__':
  Marginalization(4, True)
