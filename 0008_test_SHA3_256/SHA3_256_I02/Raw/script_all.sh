for i in $(seq -f "%04g" 0 19)
  do
    Name='https://www.cl.cam.ac.uk/research/security/datasets/sha3-32bit/Data/0008_test_SHA3_256/SHA3_256_I02/Raw/Raw_SHA3_256_I02_'${i}'.zip'
    wget $Name
  done
