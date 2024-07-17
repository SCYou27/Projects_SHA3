mkdir ../Processed_HDF5/
mkdir data_raw_in/
mkdir data_raw_out/
python3 pre_processing.py 0 10
zip data_raw_in.zip -r data_raw_in/
zip data_raw_out.zip -r data_raw_out/
rm -r data_raw_in/ data_raw_out/ __pycache__/
python3 combine_I01.py combine 0 1
python3 combine_I01.py check 0 1
python3 combine_I01.py check 0 1 >> check_report.txt
rm ../Processed_HDF5/Processed_*.hdf5
