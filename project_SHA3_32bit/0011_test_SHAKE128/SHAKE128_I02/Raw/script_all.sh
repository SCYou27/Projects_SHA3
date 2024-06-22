for i in $(seq -f "%04g" 0 19)
  do
    Name='https://www.cl.cam.ac.uk/research/security/datasets/sha3-32bit/Data/0011_test_SHAKE128/SHAKE128_I02/Raw/Raw_SHAKE128_I02_'${i}'.zip'
    wget $Name
  done
