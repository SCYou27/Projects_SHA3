import numpy as np
import os
import sys

###################################################################################
#
# Independent parameters
# Invocation number:
INVOC = 1
###################################################################################

Dict = {2500:'2500', 10000:'10000', 40000:'40000', 160000:'160000', 640000:'640000', 2560000:'failed', -1:'skipped'}

def find_success(lower, upper):
  print('=============================================================================')
  Number_Inputs = upper-lower
  Count = 0
  for t in range(lower, upper):
    if bool(np.load('Success/success_'+str(t).zfill(4)+'.npy')):
      Count += 1
  print('Successfully recovered: '+str(Count)+'/'+str(Number_Inputs))
  print('Success rate: {:0.3f}%'.format(100*Count/Number_Inputs))
  return

def capacity_statistics(lower, upper):
  print('=============================================================================')
  Number_Traces = (upper-lower)*INVOC
  Capacities = []
  for t in range(lower, upper):
    caps = np.load('Capacities/capacity_'+str(t).zfill(4)+'.npy')
    for inv in range(0, INVOC):
      Capacities.append(caps[inv])
  Cap_str = []
  Numbers = []
  Cummulated = []
  Line1 = '$T$'
  Line2 = 'new traces recovered'
  Line3 = 'cumulative percentage'
  for cap in [2500, 10000, 40000, 160000, 640000, 2560000, -1]:
    Cap_str.append(Dict[cap])
    Numbers.append(Capacities.count(cap))
    Cummulated.append(100*sum(Numbers)/Number_Traces)
  for t in range(0, len(Cap_str)):
    Line1 += (' & '+Cap_str[t])
    Line2 += (' & '+str(Numbers[t]))
    Line3 += (' & {:0.3f}\\%'.format(Cummulated[t]))
  print('\\hline')
  print(Line1+'\\\\')
  print('\\hline')
  print(Line2+'\\\\')
  print('\\hline')
  print(Line3+'\\\\')
  return
      

if __name__=='__main__':
  lower = int(sys.argv[1])
  upper = int(sys.argv[2])
  find_success(lower, upper)
  capacity_statistics(lower, upper)

