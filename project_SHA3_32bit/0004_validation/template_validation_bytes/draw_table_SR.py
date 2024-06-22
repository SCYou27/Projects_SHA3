import numpy as np
import sys

Dir_Name = "./Rank_O010/"

def Draw(func, outname, L, U):
  Ranks = []
  Tnum = 1000.0*(U-L)
  if (func[0]=='A')or(func[0]=='B'):
    Size = 200
    N_lane = 25
  elif (func[0]=='C')or(func[0]=='D'):
    Size = 40
    N_lane = 5
  for b in range(0, Size):
    Ranks.append([])
  for b in range(0, Size):
    print(("Byte #"+str(b).zfill(3)))
    byte_head = Dir_Name+"rank_"+func+"_b"+str(b).zfill(3)
    for sets in range(L, U):
      filename = byte_head+"_s"+str(sets).zfill(3)+".npy" 
      res = np.load(filename)
      for t in range(0, len(res)):
        Ranks[b].append(res[t])
  Output_str = "\\begin{tabular}{|c|*{8}{r|}}\n\\hline\n\\backslashbox{$(i,j)$}{$k$} "
  for k in range(0, 8):
    Output_str += ("&\n\\multicolumn{1}{c|}{"+str(k)+"}")
  Output_str += "\\\\\n\\hline\n"
  for lane in range(0, N_lane):
    lan_str = "("+str((lane%5))+", "+str(lane//5)+")"
    for bt in range(0, 8):
      byte = 8*lane+bt
      #print byte
      num = Ranks[byte].count(0)
      num = num/Tnum
      temp = (format(num, '0.3f')).zfill(7)
      if temp[0]=='0':
        if temp[1]=='0':
          temp = '\\0\\0'+temp[2:]
        else:
          temp = '\\'+temp
      lan_str += (" & "+temp)
    lan_str += "\\\\\n\\hline\n"
    Output_str += lan_str
  Output_str += "\\end{tabular}"
  print(Output_str)
  ofile = open(outname, "w")
  ofile.write(Output_str)
  ofile.close()

if __name__=='__main__':
  Func = sys.argv[1]
  Group = int(sys.argv[2])
  Otn = "Result_Tables/SR_table_"+Func+"_G"+str(Group)+".txt"
  Lower = Group
  Upper = Group+1
  Draw(Func, Otn, Lower, Upper)

