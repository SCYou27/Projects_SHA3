import numpy as np
import sys
class State_Prob:
  def __init__(self, Size=1600):
    self.Size = Size
    self.PreviousEntropy = 0.5*np.ones((2, self.Size))
    return
  
  def renew(self, Table):
    Total_Prob = np.array(Table)
    abs_total_D = np.sum(abs(Total_Prob-self.PreviousEntropy))
    self.PreviousEntropy = Total_Prob
    return abs_total_D

