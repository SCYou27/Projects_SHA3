Step 1: All-in-one script:
	./script_all.sh

Step 2: Initialization (get templates, interesting clock cycles, answers):
	./init.sh

Step 3: Clean to restart:
	./clean.sh

Step 3: Testing procedure:
	python3 SASCA_Procedure.py 0 1000

Step 4: Print the results:
	python3 calculate_data_new.py 0 1000

Step 5: Clean the dependant data:
	./pack.sh

