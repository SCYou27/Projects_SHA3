BOUND='010'
unzip ../Code_intermediate_values/intermediate_values.zip
unzip ../../0002_detection/Code_extract_ics/ics_original_${BOUND}.zip
unzip ../../0003_training/template_profiling_bytes/templateLDA_O${BOUND}.zip
mkdir Rank_O${BOUND}/
python3 validate_script.py 0 4
zip Rank_O${BOUND}.zip -r Rank_O${BOUND}/
mkdir Result_Tables/ 
python3 draw_all.py 4
zip Result_Tables.zip -r Result_Tables/
rm -r intermediate_values/ templateLDA_O*/ ics_*/ __pycache__/ Rank_O*/ Result_Tables/
