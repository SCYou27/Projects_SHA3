import os
import sys
import numpy as np
trace_num = 16000

Tr_Mat = np.matrix([[128],[64],[32],[16],[8],[4],[2],[1]])

str2num = {'0': 0, '1': 1, '2': 2, '3': 3,\
           '4': 4, '5': 5, '6': 6, '7': 7,\
           '8': 8, '9': 9, 'a':10, 'b':11,\
           'c':12, 'd':13, 'e':14, 'f':15 }

def intermediate_translate(tag):
  if tag[0]=='A' or tag[0]=='B' or tag[0]=='E':
    Size = 200
  elif tag[0]=='C' or tag[0]=='D':
    Size = 40
  else:
    print("Error: wrong tag.")
    return
  InterBits = []
  for b in range(0, Size):
    InterBits.append([])
  inname = "Invocation_IO/intermediate_H_"+tag+".npy"
  out_dir = "intermediate_values/intermediate_B_"+tag+"/"
  os.system(("mkdir "+out_dir))
  Str_In = np.load(inname)
  for t in range(0, trace_num):
    print("Processing trace #"+str(t))
    in_str = Str_In[t]
    for b in range(0, Size):
      bits = [-1.0]*8
      byte = str2num[(in_str[(2*b)])]*16+str2num[(in_str[(2*b+1)])]
      bit_str = bin(byte)[2:].zfill(8)
      for bt in range(0, 8):
        bits[bt] = float(bit_str[bt])
      InterBits[b].append(bits)
  for b in range(0, Size):
    outname = out_dir+tag+"_b"+str(b).zfill(3)+".npy"
    print("Saving "+outname)
    np.save(outname, InterBits[b])
  return

def checking(tag):
  if tag[0]=='A' or tag[0]=='B' or tag[0]=='E':
    Size = 200
  elif tag[0]=='C' or tag[0]=='D':
    Size = 40
  else:
    print("Error: wrong tag.")
    return
  hex_name = "Invocation_IO/intermediate_H_"+tag+".npy"
  byte_dir = "intermediate_values/intermediate_B_"+tag+"/"
  Str_hex = np.load(hex_name)
  for b in range(0, Size):
    byte_name = byte_dir+tag+"_b"+str(b).zfill(3)+".npy"
    X_byte = np.load(byte_name)
    ANS = X_byte*Tr_Mat
    for t in range(0, trace_num):
      x_hex = Str_hex[t][(2*b):(2*b+2)]
      x_byte = hex(int(ANS.item(t)))[2:].zfill(2)
      #print(b, t, x_hex, x_byte)
      if x_hex!=x_byte:
        print("Error:", b, t)
        exit()
  return tag+": ALL PASSED."
        
if __name__=='__main__':
  Func = sys.argv[1]
  for tag in ['A', 'B', 'C', 'D', 'E']:
    for rd in range(0, 4):
      Tag = tag+str(rd).zfill(2)
      if Func=='cal':
        intermediate_translate(Tag)
      elif Func=='check':
        print(checking(Tag))


