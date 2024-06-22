for i in $(seq -f "%04g" 0 19)
  do
    Name='https://www.cl.cam.ac.uk/research/security/datasets/sha3-32bit/Data/0010_test_SHAKE256/SHAKE256_I02/Raw/Raw_SHAKE256_I02_'${i}'.zip'
    wget $Name
  done
