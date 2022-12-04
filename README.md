# Cryptosystems
This is my project work for a discrete math course. It is a command line tool that can encrypt and decrypt  text using three different encryption algorithms: the affine cipher, the transposition cipher and RSA. The usage and theoretical background of each algorithm is mentioned below.

## THE AFFINE CIPHER
This is the sequence of command line arguments to use for the affine cipher

    python cryptosystems.py affine en "[plainText]" .... to encrypt
    python cryptosystems.py affine de "[cipherText]" ..... to decrypt

The affine cipher is a generalization of shift ciphers with the form f(p) = (ap + b) mod 26
where a and b are parts of the key and gcd(a, 26) = 1. in out code, we use a=15 qne b=21. of 
course, these values can be changed in the code. The function: f(p) = (ap + b) mod 26 is the 
encryption function. to get the decryption function, we use the encrypting congruence and 
express p in terms of f(p). this involves working out the inverse of a modulo 26. we use the 
helper function inverse_mod_m to achieve that.



## THE TRANSPOSITION CIPHER
this is the sequence of command line arguments to use the transposition cipher

    python cryptosystems.py transposition en "[plainText]" ... to encrypt
    python cryptosystems.py transposition de "[cipherText]" ... to decrypt

the transposition cipher is a block cipher. the encryption function maps the position of 
letters in a block to a permutation of the set (1,2,3 ... m) where m is the block legth. 
what we take as a key is this permutation. the key is set in the code to [2,0,3,1]. of course, 
this key can be changed in the code. to encrypt, we apply the encryption function.
to decrypt, we use the inverse of the mapping. This process is very similar to the encryption
with the main difference being the key used. for decryption, we use the inverse key. the
functionality to make the inverse key is built into the decrypt method. the decrypt method
then simply calls the encrypt method, passing it the inverse key. this results in the cipherText
being decrypted.


## THE RSA CIPHER
this is the sequence of command line arguments to use the RSA cipher

    python cryptosystems.py rsa en [plainLetter] .... to encrypt
    python cryptosystems.py rsa de [cipherLetter] .... to decrypt

the RSA is a modern public key encryption system that is based on the dificulty to factor a  large 
number into its prime factors. In the code, the constructor of the RSA class takes a public key in
the form of a tuple: (m, a) where m is a product of two large primes p and q. also, a must be coprime
with (p-1)*(q-1). the constructor also takes the two primes p and q. because these two primes are 
known to the constructor, the constructor can make out and set the private key. a can be considered
as the encryption exponent because the encryption function is: f(p) = (p^a) mod m. The process of
making out the private key mainly involves finding the decryption exponent d. d can be found by working
out the inverse of a modulo (p-1)*(q-1). d is considered the decryption exponent becuase the decryption
function is: f(p) = (p^d) mod m. The public key is set in the code as (253, 7) with p and q being
11 and 23 respectively. of course, this can be changed in the code.

The RSA cipher implemented in the code encrypts and decrypts only single characters while the other two ciphers can encrypt and decrepit strings.
