unzip Rank_C090.zip
mkdir Result_Tables/ 
python3 draw_all.py 2
zip Result_Tables.zip -r Result_Tables/
rm -vr Rank_C*/ Result_Tables/
