for i in $(seq -f "%04g" 0 39)
  do
    Name='https://www.cl.cam.ac.uk/research/security/datasets/sha3-32bit/Data/0004_validation/Raw/Raw_TS_'${i}'.zip'
    wget $Name
  done
