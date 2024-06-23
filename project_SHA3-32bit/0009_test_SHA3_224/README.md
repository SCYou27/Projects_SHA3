# Attack on the SHA3-224 hash function

The main goal of tasks in "0009_SHA3-224/" is to perform Soft Analytical Side-Channel Attack (SASCA) on the SHA3-224 hash function.

Although we built our templates with traces recorded during SHA3-512 executions, we believe these templates can be used to attack other three hash and two extendable-output functions in SHA-3 because our attack method focus on the internal states in the Keccak-_f_[1600] permutations, which remain unchanged across these six different functions.

Like the case of the attack on SHA3-512, we separate this data set into the following two subsets by the number of invocations required:

 - "SHA3_224_I01/": attack on 1000 executions of SHA3-224 with one invocation of Keccak permutation.
 - "SHA3_224_I02/": attack on 1000 executions of SHA3-224 with two invocations of Keccak permutation.

Please check the README.md file in each sub-directory for more instructions.


