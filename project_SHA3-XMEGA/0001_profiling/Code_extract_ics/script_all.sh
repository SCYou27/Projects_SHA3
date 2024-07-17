unzip ../Code_detection_R2/detect_results_08.zip
python3 ics_detect.py 0.64
python3 ics_detect.py 0.49
python3 ics_detect.py 0.36
python3 ics_detect.py 0.25
python3 ics_detect.py 0.16
python3 ics_detect.py 0.09
python3 ics_combine.py 640
python3 ics_combine.py 490
python3 ics_combine.py 360
python3 ics_combine.py 250
python3 ics_combine.py 160
python3 ics_combine.py 090
rm -r detect_results_*/ __pycache__/
