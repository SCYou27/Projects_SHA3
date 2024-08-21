import numpy as np
import sys
import time
import heapq

#Dummy = np.array([-1.0, -float('inf')])

class Terminal:
  def __init__(self, Table):
    self.RankTable = []
    for t in range(0, len(Table[0])):
      heapq.heappush(self.RankTable, (Table[0][t][1], list(map(int, Table[0][t][0]) if type(Table[0][t][0]) is list else [int(Table[0][t][0])])))
    self.ended = False
    self.dummy = (float('inf'), [-1]*len(self.RankTable[0][1]))
    return
  
  def Next_one(self):
    if self.ended:
      return self.dummy
    try:
      return heapq.heappop(self.RankTable)
    except:
      self.ended = True
      return self.dummy

class Node:
  def __init__(self, Table):
    self.ended = False
    Mid = (len(Table)//2)
    if len(Table[:Mid])==1:
      self.LChild = Terminal(Table[:Mid])
    else:
      self.LChild = Node(Table[:Mid])
    if len(Table[Mid:])==1:
      self.RChild = Terminal(Table[Mid:])
    else:
      self.RChild = Node(Table[Mid:])
    temp_list = self.LChild.dummy[1]+self.RChild.dummy[1]
    self.dummy = (float('inf'), temp_list)
    self.Fronts = []
    self.LTable = []
    self.RTable = []
    self.LTable.append(self.LChild.Next_one())
    self.RTable.append(self.RChild.Next_one())
    Prob = self.LTable[0][0]+self.RTable[0][0]
    Indeces = (0,0)
    Bytes = self.LTable[0][1]+self.RTable[0][1]
    Element = []
    Element.append(Prob)
    Element.append(Indeces)
    Element.append(Bytes)
    heapq.heappush(self.Fronts, (Prob, Indeces, Bytes))
    self.Front_ID_L = [True]
    self.Front_ID_R = [True]
    return
  
  def Next_one(self):
    if self.ended:
      return self.dummy
    try:
      (Next_Prob, (Next_L, Next_R), Next_Bytes) = heapq.heappop(self.Fronts)
      if Next_Prob==float('inf'):
        self.ended = True
        return self.dummy
    except:
      self.ended = True
      return self.dummy
    Output = (Next_Prob, Next_Bytes)
    self.Front_ID_L[Next_L] = False
    self.Front_ID_R[Next_R] = False
    #==============Table Expanation=================
    if Next_R==0:
      self.LTable.append(self.LChild.Next_one())
      self.Front_ID_L.append(False)
    if Next_L==0:
      self.RTable.append(self.RChild.Next_one())
      self.Front_ID_R.append(False)
    #===============================================
    if (self.Front_ID_L[(Next_L+1)]==False)and(self.Front_ID_R[(Next_R)]==False):
      Prob = self.LTable[Next_L+1][0]+self.RTable[Next_R][0]
      Bytes = self.LTable[Next_L+1][1]+self.RTable[Next_R][1]
      heapq.heappush(self.Fronts, (Prob, (Next_L+1, Next_R), Bytes))
      self.Front_ID_L[Next_L+1] = True
      self.Front_ID_R[Next_R] = True
    if (self.Front_ID_L[(Next_L)]==False)and(self.Front_ID_R[(Next_R+1)]==False):
      Prob = self.LTable[Next_L][0]+self.RTable[Next_R+1][0]
      Bytes = self.LTable[Next_L][1]+self.RTable[Next_R+1][1]
      heapq.heappush(self.Fronts, (Prob, (Next_L, Next_R+1), Bytes))
      self.Front_ID_L[Next_L] = True
      self.Front_ID_R[Next_R+1] = True
    return Output


class Enumerator:
  def __init__(self, GreatTable):
    self.count = 0
    self.INnode = Node(GreatTable) 
    return
  
  def Next_one(self):
    (dist, candidates) = self.INnode.Next_one()
    self.count+=1
    return candidates, dist

if __name__=='__main__':
  T_1 = [[0.0, 13467.2], [1.0, 123545.7], [2.0,  88832.2]]
  T_2 = [[0.0, 73467.2], [1.0,  13545.7], [2.0, 842352.2]]
  T_3 = [[0.0,   737.2], [1.0, 213545.7], [2.0,     52.2]]
  enumerator = Enumerator([T_1, T_2, T_3])
  dist = 0.0
  counter = 0
  while dist<float('inf'):
    cand, dist = enumerator.Next_one()
    print(counter, cand, '{:0.3f}'.format(dist))
    counter+=1
