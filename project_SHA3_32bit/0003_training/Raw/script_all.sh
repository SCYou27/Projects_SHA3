for i in $(seq -f "%04g" 0 399)
  do
    Name='https://www.cl.cam.ac.uk/research/security/datasets/sha3-32bit/Data/0003_training/Raw/Raw_TR_'${i}'.zip'
    wget $Name
  done
