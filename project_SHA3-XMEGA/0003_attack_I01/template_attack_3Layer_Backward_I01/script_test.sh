./init.sh
python3 Search_Procedure.py 0 10
python3 statistics.py 0 10
python3 statistics.py 0 10 > report.txt
./pack.sh
