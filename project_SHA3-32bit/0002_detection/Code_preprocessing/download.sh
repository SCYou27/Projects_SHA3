DIR='https://www.cl.cam.ac.uk/research/security/datasets/sha3-32bit/Data/0002_detection/'
mkdir ../Processed_HDF5/
for part in $(seq -f "%02g" 0 3)
  do
    wget ${DIR}Processed_HDF5/part_${part}.hdf5 -P ../Processed_HDF5/
  done
wget ${DIR}Code_preprocessing/data_raw_in.zip
wget ${DIR}Code_preprocessing/data_raw_out.zip
wget ${DIR}Code_preprocessing/Corrcoefs.zip
wget ${DIR}Code_preprocessing/check_report.txt
