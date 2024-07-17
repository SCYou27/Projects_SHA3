for i in $(seq -f "%03g" 0 19)
  do
    Name='https://www.cl.cam.ac.uk/research/security/datasets/sha3-XMEGA/Data/Raw/eval4/sha3_test_set_'${i}'.zip'
    wget $Name
  done
