for i in $(seq -f "%03g" 0 9)
  do
    Name='https://www.cl.cam.ac.uk/research/security/datasets/sha3-XMEGA/Data/Raw/test1/sha3_test1_set_'${i}'.zip'
    wget $Name
  done
