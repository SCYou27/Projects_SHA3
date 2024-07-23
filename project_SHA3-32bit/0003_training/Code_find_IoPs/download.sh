DIR='https://www.cl.cam.ac.uk/research/security/datasets/sha3-32bit/Data/0003_training/Code_find_IoPs/'
mkdir IoPs/
for rd in $(seq -f "%02g" 0 3)
  do
    for word in $(seq -f "%02g" 0 49)
      do
        wget ${DIR}IoPs/Ints_A${rd}_i${word}.hdf5 -P IoPs/
      done
    for word in $(seq -f "%02g" 0 49)
      do
        wget ${DIR}IoPs/Ints_B${rd}_i${word}.hdf5 -P IoPs/
      done
    for word in $(seq -f "%02g" 0 9)
      do
        wget ${DIR}IoPs/Ints_C${rd}_i${word}.hdf5 -P IoPs/
      done
    for word in $(seq -f "%02g" 0 9)
      do
        wget ${DIR}IoPs/Ints_D${rd}_i${word}.hdf5 -P IoPs/
      done
  done
