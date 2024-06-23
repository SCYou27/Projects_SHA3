# Belief propagation testing

The main goal of tasks in "0005_SASCA/" is to test the factor graphs for belief propagation within a single Keccak-f[1600] permutation, which is associated with Fig. 4. in our paper. We did not record additional traces but just use the first 1000 in the validation set ("0004_validation/") for this phase.

1. Find answer bits for two states:

	`cd get_answers/`  
	`./script_all.sh`  

   This task extracts the answer bits for the input state and intermediate state A00 from the 1000 validation traces. We need the former to generate probability tables for the input capacity part and the latter to check if the belief propagation procedure stablizes and converges to the correct bit values.

2. Marginalized bit tables generation:

	`cd bit_table_generation/`  
	`./script_all.sh`  

   This step will first perform template attack to build probability tables for intermediate bytes, and then marginalize them into bitwise tables (archived in "Bit_Tables.zip"). Note that we did not build templates for the input state but used the answer bits generated in the previous task to generate the probability tables for the input bitwise tables (by setting the correct candidate bit with probability equal to 1, whereas the other with 0).

3. Find success rate given different numbers of iterations with factor graphs covering 2, 3, or 4 rounds:

	`cd Iteration_Scan_2R/` (or `cd Iteration_Scan_3R/`, `cd Iteration_Scan_4R/`)  
	`./script_all.sh`  

   Based on the extracted I/O data, this step will calculate our target intermediate values and store them in bytes as the answers for the quality evaluation.

4. Template validation:

	`cd template_validation_bytes/`  
	`./script_all.sh`  

   This step is to evaluate the quality of templates by providing a success rate and guessing entropy. The results will be stored in "template_validation_bytes/Result_Tables.zip"

   You can compare the numbers in Tables 2, 3, 4, and 5 in our paper with the following files:

   - Result_Tables/SR_table_A00_G0.txt
   - Result_Tables/GE_table_A00_G0.txt
   - Result_Tables/SR_table_B00_G0.txt
   - Result_Tables/GE_table_B00_G0.txt
   - Result_Tables/SR_table_C00_G0.txt
   - Result_Tables/GE_table_C00_G0.txt
   - Result_Tables/SR_table_D00_G0.txt
   - Result_Tables/GE_table_D00_G0.txt
