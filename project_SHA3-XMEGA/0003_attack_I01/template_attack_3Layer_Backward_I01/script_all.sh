./init.sh
python3 Search_Procedure.py 0 1000
python3 statistics.py 0 1000
python3 statistics.py 0 1000 > report.txt
./pack.sh
