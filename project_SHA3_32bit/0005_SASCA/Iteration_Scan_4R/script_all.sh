lower=0
upper=1000
./init.sh
python3 Iteration_scan.py ${lower} ${upper}
python3 get_results.py ${lower} ${upper}
./pack.sh
