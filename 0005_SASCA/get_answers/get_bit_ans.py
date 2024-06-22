import numpy as np

str2num = {'0': 0, '1': 1, '2': 2, '3': 3,\
           '4': 4, '5': 5, '6': 6, '7': 7,\
           '8': 8, '9': 9, 'a':10, 'b':11,\
           'c':12, 'd':13, 'e':14, 'f':15 }

Array = 2**np.array(range(0, 8)) 

def str2bytes(my_string):
  if len(my_string)%2==1:
    print('Warning: not a byte string')
    exit()
  Bytes = []
  for t in range(0, len(my_string)//2):
    Bytes.append((16*str2num[my_string[2*t]]+str2num[my_string[2*t+1]]))
  return Bytes

def byte2bits(my_byte):
  return (my_byte&Array)//Array

def get_answer(my_string):
  Bytes = str2bytes(my_string)
  table_O = []
  for t in range(0, len(Bytes)):
    table_O.append(byte2bits(Bytes[t]))
  return np.hstack(table_O)

def processing(input_name, output_dir, L, U):
  print('================================================================')
  print(input_name)
  strings = np.load(input_name)
  for t in range(L, U):
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    my_string = strings[t]
    print('#'+str(t).zfill(4)+': '+my_string)
    fname = output_dir+'ans_bit_'+str(t).zfill(4)+'.npy'
    np.save(fname, get_answer(my_string))
  return

if __name__=='__main__':
  processing('Invocation_IO/trace_input.npy',        'answer_bit/answers_INP/', 0, 1000)
  processing('Invocation_IO/intermediate_H_A00.npy', 'answer_bit/answers_A00/', 0, 1000)
