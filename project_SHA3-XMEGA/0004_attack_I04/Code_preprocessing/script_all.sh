mkdir ../Processed_HDF5/
mkdir data_raw_in/
mkdir data_raw_out/
python3 pre_processing.py 20 60
zip data_raw_in.zip -r data_raw_in/
zip data_raw_out.zip -r data_raw_out/
rm -r data_raw_in/ data_raw_out/ __pycache__/
python3 combine_I04.py combine 0 4
python3 combine_I04.py check 0 4
python3 combine_I04.py check 0 4 >> check_report.txt
rm ../Processed_HDF5/Processed_*.hdf5
