for i in $(seq -f "%03g" 0 199)
  do
    Name='https://www.cl.cam.ac.uk/research/security/datasets/sha3-XMEGA/Data/Raw/train/sha3_train_set_'${i}'.zip'
    wget $Name
  done
