lower=0
upper=200
part=20
mkdir ../Processed_HDF5/
mkdir ../Peaks_HDF5/
mkdir data_raw_in/
mkdir data_raw_out/
python3 pre_processing.py ${lower} ${upper}
zip data_raw_in.zip -r data_raw_in/
zip data_raw_out.zip -r data_raw_out/
rm -r data_raw_in/ data_raw_out/ __pycache__/
python3 combine_DN.py combine 0 2
python3 combine_DN.py check 0 2
python3 combine_DN.py check 0 2 >> check_report.txt
python3 combine_TR.py combine 0 ${part}
python3 combine_TR.py check 0 ${part}
python3 combine_TR.py check 0 ${part} >> check_report.txt
rm ../Peaks_HDF5/Processed_*.hdf5
rm ../Processed_HDF5/Processed_*.hdf5
