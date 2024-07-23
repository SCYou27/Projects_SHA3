DIR='https://www.cl.cam.ac.uk/research/security/datasets/sha3-32bit/Data/0002_detection/Code_extract_ics/'
for i in {1..9}
  do
    wget ${DIR}ics_original_0${i}'0.zip'
  done
wget ${DIR}Tables.zip
