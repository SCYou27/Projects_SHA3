# Attack on the SHA3-384 hash function

The main goal of the tasks in "0007\_test\_SHA3-384/" is to perform Soft Analytical Side-Channel Attack (SASCA) on the SHA3-384 hash function.

Although we built our templates with traces recorded during SHA3-512 executions, we believe these templates can be used to attack other three hash and two extendable-output functions in SHA-3 because our attack method focuses on the internal states in the Keccak-_f_[1600] permutations, which remain unchanged across these six different functions.

Like the case of the attack on SHA3-512, we divided this data set into the following two subsets by the number of invocations required:

 - "SHA3\_384\_I01/": attack on 1000 executions of SHA3-384 with one invocation of Keccak permutation.
 - "SHA3\_384\_I02/": attack on 1000 executions of SHA3-384 with two invocations of Keccak permutation.

Please check the README.md file in each sub-directory for more instructions.


