BOUND='090'
unzip ../Code_intermediate_values/intermediate_values.zip
unzip ../../0001_profiling/Code_extract_ics/ics_combined_${BOUND}.zip
unzip ../../0001_profiling/template_profiling_bytes/templateLDA_C${BOUND}.zip
mkdir Rank_C${BOUND}/
python3 validate_script.py 0 2
zip Rank_C${BOUND}.zip -r Rank_C${BOUND}/
mkdir Result_Tables/ 
python3 draw_all.py 2
zip Result_Tables.zip -r Result_Tables/
rm -r intermediate_values/ templateLDA_C*/ ics_*/ __pycache__/ Rank_C*/ Result_Tables/
