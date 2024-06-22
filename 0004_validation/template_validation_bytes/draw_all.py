import os
import sys
def process(N_group):
  Tag = ['A', 'B', 'C', 'D']
  RD = ['00', '01', '02', '03']
  TB = ['SR', 'GE']
  for G in range(0, N_group):
    for T in Tag:
      for R in RD:
        for N in TB:
          cmd = "python3 draw_table_"+N+".py "+T+R+" "+str(G)
          print(cmd)
          os.system(cmd)
  return

if __name__=='__main__':
  process(int(sys.argv[1]))


