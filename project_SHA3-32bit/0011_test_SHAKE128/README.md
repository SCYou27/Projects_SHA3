# Attack on the SHAKE128 extendable-output function (XOF)

The main goal of the tasks in "0011_SHAKE128/" is to perform a Soft Analytical Side-Channel Attack (SASCA) on the SHAKE128 extendable-output function (XOF).

Although we built our templates with traces recorded during SHA3-512 executions, we believe these templates can be used to attack other three hash and two extendable-output functions in SHA-3 because our attack method focuses on the internal states in the Keccak-_f_[1600] permutations, which remain unchanged across these six different functions.

Like the case of the attack on SHA3-512, we separate this data set into the following two subsets by the number of invocations required:

 - "SHAKE128_I01/": attack on 1000 executions of SHAKE128 with one invocation of Keccak permutation.
 - "SHAKE128_I02/": attack on 1000 executions of SHAKE128 with two invocations of Keccak permutation.

However, unlike the fixed-length output from SHA-3 hash functions, the two XOFs require users to indicate an output length they need. For our experiments, we request a 168-byte output from the target SHAKE128 function. This is equal to the rate size of this sponge function, so it will not invoke additional permutations in the squeezing stage.  

Please check the README.md file in each sub-directory for more instructions.


