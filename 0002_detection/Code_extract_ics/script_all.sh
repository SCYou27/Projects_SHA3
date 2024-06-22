unzip ../Code_detection_R2/detect_results_32.zip
mkdir Tables/
python3 ics_detect.py 0.09
python3 ics_detect.py 0.08
python3 ics_detect.py 0.07
python3 ics_detect.py 0.06
python3 ics_detect.py 0.05
python3 ics_detect.py 0.04
python3 ics_detect.py 0.03
python3 ics_detect.py 0.02
python3 ics_detect.py 0.01
python3 draw_tables.py
zip -qq Tables.zip -r Tables/
rm -r detect_results_*/ Tables/
