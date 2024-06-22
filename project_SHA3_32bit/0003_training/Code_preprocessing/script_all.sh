lower=0
upper=400
part=16
mkdir ../Processed_HDF5/
mkdir Corrcoefs/
mkdir data_raw_in/
mkdir data_raw_out/
python3 pre_processing.py ${lower} ${upper}
python3 check_corr.py 0.99 ${lower} ${upper}
python3 check_corr.py 0.99 ${lower} ${upper} > check_report.txt
zip Corrcoefs.zip -r Corrcoefs/
zip data_raw_in.zip -r data_raw_in/
zip data_raw_out.zip -r data_raw_out/
rm -r Corrcoefs/ data_raw_in/ data_raw_out/ __pycache__/
python3 combine.py combine 0 ${part}
python3 combine.py check 0 ${part}
python3 combine.py check 0 ${part} >> check_report.txt
rm ../Processed_HDF5/Processed_*.hdf5
