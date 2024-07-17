mkdir intermediate_values/
mkdir Invocation_IO/
unzip ../Code_preprocessing/data_raw_in.zip
unzip ../Code_preprocessing/data_raw_out.zip
python3 get_invoc_io.py cal
python3 get_invoc_io.py check
python3 get_invoc_io.py check > check_report_IO.txt
python3 get_invoc_intermediate.py
python3 intermediate_H2B.py cal
python3 intermediate_H2B.py check
python3 intermediate_H2B.py check > check_report_bytes.txt
zip Invocation_IO.zip -r Invocation_IO/
zip intermediate_values.zip -r intermediate_values/
rm -r data_raw_in/ data_raw_out/ Invocation_IO/ intermediate_values/ __pycache__/

