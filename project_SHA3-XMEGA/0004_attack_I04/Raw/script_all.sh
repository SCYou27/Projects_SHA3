for i in $(seq -f "%03g" 20 59)
  do
    Name='https://www.cl.cam.ac.uk/research/security/datasets/sha3-XMEGA/Data/Raw/test4/sha3_test_set_'${i}'.zip'
    wget $Name
  done
