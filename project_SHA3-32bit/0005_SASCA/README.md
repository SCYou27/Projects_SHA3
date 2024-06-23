# Belief propagation testing

The main goal of tasks in "0005_SASCA/" is to test the factor graphs for our loopy belief propagation (loopy-BP) within a single Keccak-_f_[1600] permutation, which is associated with Fig. 4. in our paper. With the factor graphs covering the first 2, 3, or 4 rounds out of the total 24 rounds within an invocation of Keccak-_f_[1600], we provide the success rate to reconstruct the A00 intermediate state, over different numbers of loopy-BP iterations and varying values of rate and corresponding capacity (_c_ = 1600-_r_).


We did not record additional traces but used the first 1000 in the validation set ("0004\_validation/") for this phase.

1. Find answer bits for two states:

	`cd get_answers/`  
	`./script_all.sh`  

   This task extracts the answer bits for the input state and intermediate state A00 from the 1000 validation traces. We need the former to generate probability tables for the input capacity part and the latter to check if the belief propagation procedure stabilizes and converges to the correct bit values.

2. Marginalized bit tables generation:

	`cd bit_table_generation/`  
	`./script_all.sh`  

   This step will first perform a template attack to build probability tables for intermediate bytes and then marginalize them into bitwise tables (archived in "Bit\_Tables.zip"). Note that we did not build templates for the input state but used the answer bits generated in the previous task to generate the probability tables for the input bitwise tables (by setting the correct candidate bit with probability equal to 1, whereas the other with 0).

3. Find the success rate given different numbers of BP iterations with factor graphs covering 2, 3, or 4 rounds:

	`cd Iteration_Scan_2R/` (or `cd Iteration_Scan_3R/`, `cd Iteration_Scan_4R/`)  
	`./script_all.sh`  

4. Find the success rate given varying values of rate and capacity with factor graphs covering 2, 3, or 4 rounds:

	`cd Rate_Scan_2R/` (or `cd Rate_Scan_3R/`, `cd Rate_Scan_4R/`)  
	`./script_all.sh`  

   Note that rate will be the number of bits in the input state without information, which means that we assign the probability of both candidates for these bits to be 0.5, while we assign the others (capacity part) with the values calculated in task "bit\_table\_generation/".

5. Plot the results:

	`cd plot_scans/`  
	`./script_all.sh`  

   This will plot the results in two figures: "SuccessOverIteration.pdf" and "SuccessOverRate.pdf".

