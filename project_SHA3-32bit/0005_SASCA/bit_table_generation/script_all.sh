lower=0
upper=1000
./init.sh
python3 get_tables.py ${lower} ${upper}
./pack.sh
