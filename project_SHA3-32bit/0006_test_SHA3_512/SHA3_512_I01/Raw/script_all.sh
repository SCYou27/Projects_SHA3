for i in $(seq -f "%04g" 0 9)
  do
    Name='https://www.cl.cam.ac.uk/research/security/datasets/sha3-32bit/Data/0006_test_SHA3_512/SHA3_512_I01/Raw/Raw_SHA3_512_I01_'${i}'.zip'
    wget $Name
  done
