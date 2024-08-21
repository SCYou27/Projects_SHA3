DIR='https://www.cl.cam.ac.uk/research/security/datasets/sha3-32bit/Data/0007_test_SHA3_384/SHA3_384_I02/'
mkdir ../Processed_HDF5/
for part in $(seq -f "%02g" 0 1)
  do
    wget ${DIR}Processed_HDF5/Invocation_${part}.hdf5 -P ../Processed_HDF5/
  done
wget ${DIR}Code_preprocessing/data_raw_in.zip
wget ${DIR}Code_preprocessing/data_raw_out.zip
wget ${DIR}Code_preprocessing/Corrcoefs.zip
wget ${DIR}Code_preprocessing/check_report.txt