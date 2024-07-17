import os
import sys
def process(N_group):
  Tag = ['A00', 'B00', 'E01', 'B01']
  for G in range(0, N_group):
    for T in Tag:
      for N in ['SR', 'GE']:
        cmd = "python3 draw_table_"+N+".py "+T+" "+str(G)
        print(cmd)
        os.system(cmd)
  return

if __name__=='__main__':
  process(int(sys.argv[1]))


