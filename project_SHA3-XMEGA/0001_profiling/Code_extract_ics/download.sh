DIR='https://www.cl.cam.ac.uk/research/security/datasets/sha3-XMEGA/Data/0001_profiling/Code_extract_ics/'
for tag in '090' '160' '250' '360' '490' '640'
  do
    wget ${DIR}ics_original_${tag}.zip
    wget ${DIR}ics_combined_${tag}.zip
  done
