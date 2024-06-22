./init.sh
python3 SASCA_Procedure.py 0 1000
python3 calculate_data_new.py 0 1000
python3 calculate_data_new.py 0 1000 > report.txt
./pack.sh
