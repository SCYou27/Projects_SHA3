unzip Rank_O010.zip
mkdir Result_Tables/ 
python3 draw_all.py 4
zip Result_Tables.zip -r Result_Tables/
rm -vr Rank_O*/ Result_Tables/
