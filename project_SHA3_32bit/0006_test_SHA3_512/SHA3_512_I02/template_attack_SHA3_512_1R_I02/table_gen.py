import numpy as np

hex2int = {'0': 0, '1': 1, '2': 2, '3': 3,\
           '4': 4, '5': 5, '6': 6, '7': 7,\
           '8': 8, '9': 9, 'a':10, 'b':11,\
           'c':12, 'd':13, 'e':14, 'f':15}

table_Z = np.array([[1.0, 0.0]])
table_O = np.array([[0.0, 1.0]])

def find_int(h_str):
  int_t = 0
  for c in h_str:
    int_t <<= 4
    int_t += hex2int[c]
  return int_t

def find_table(h_str):
  Size = 4*len(h_str)
  int_t = 0
  for c in h_str:
    int_t <<= 4
    int_t += hex2int[c]
  Bin = bin(int_t)[2:].zfill(Size)
  Table = np.zeros((0, 2))
  for b in Bin:
    if b=='0':
      Table = np.vstack([Table, table_Z])
    else:
      Table = np.vstack([Table, table_O])
  return Table

if __name__=='__main__':
  IV = '80400c0600000000'
  print(hex(find_int(IV)))
  print(find_table(IV))
