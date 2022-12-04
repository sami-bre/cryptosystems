
import sys
from random import randint


# SOME HELPER FUNCTIONS ... 

# euclidean GCD
def gcd(dvd,dvs):
    # this is a simple euclidean GCD algorithm implemented iteratively.
    rem = dvd%dvs
    while (rem != 0):
        dvd = dvs
        dvs = rem
        rem = dvd%dvs
    return dvs


#bezout coefficients
def bezout(dvd,dvs):
    # this method finds the Bezout coefficients for the GCD of two numbers, dvd and dvs, respectively
    # we used the extended euclidean algorithm from our textbook (page 287) with a little modification.
    table = []
    rem = dvd%dvs
    table.append((0,0,0,0,0,1))     # adding the first row to the table
    table.append((dvd, dvs, dvd//dvs, rem, 1, 0))   # adding the second row
    while (rem != 0):
        dvd = dvs
        dvs = rem
        rem = dvd%dvs
        table.append((dvd, dvs, dvd//dvs, rem, table[-2][4]-(table[-2][2]*table[-1][4]), table[-2][5]-(table[-2][2]*table[-1][5])))
    return (table[-2][4]-(table[-2][2]*table[-1][4]), table[-2][5]-(table[-2][2]*table[-1][5]))

# inverse of a number modulo some number.
def inverse_mod_m(num, mod):
    if(gcd(num, mod) != 1):
        # according to theorem 1 on page 291 of the book unless num and mod are coprime, 
        # there is no guarantee the inverse exists, so we won't be doing any 
        # work unless they're coprime.
        raise Exception("the number and modulus are not coprime.")
    inv = bezout(num, mod)[0]   # the inverse will be the coefficient of num
    return inv % mod    # we want the unique inverse which is non negative and less than m


# functions to convert letter to digits and vice versa
def digit(letter):
    # this utility method converts letters to digits
    # for the sake of simplicity, we capitalize letters before converting.
    letter = str.capitalize(letter)
    return ord(letter) - 65

def letter(digit):
    # this utility method convers digits to letters
    return chr(digit+65)


# THE AFFINE CIPHER CLASS
class AffineCipher:
    def encrypt(self, plainText: str, key: tuple):
        # key[0] must be coprime with 26 for the cipher to work.
        if gcd(key[0], 26) != 1:
            raise Exception("the key is invalid. key[0] is not coprime with 26.")
        a, b = key
        cipherText = ""         # the cipher text starts out empty.
        for plainChar in plainText:
            if plainChar == " ":        # we ignore space characters.
                cipherText += plainChar
                continue
            # the code below is the function that encrypts a letter.
            # it then concatinates the encrypted letter to the cipher text.
            cipherChar = letter((a*digit(plainChar) + b) % 26)
            cipherText += cipherChar
        return cipherText

    def decrypt(self, cipherText: str, key: tuple):
        # again, key[0] must be coprime with 26 for the decryption to work.
        if gcd(key[0], 26) != 1:
            raise Exception("the key is invalid. key[0] is not coprime with 26.")
        a, b = key
        a_inv = inverse_mod_m(a, 26)    # this is the inverse of 'a' modulo 26.
        plainText = ""      # the plain text starts out empty
        for cipherChar in cipherText:
            if cipherChar == " ":       # again, we don't decrypt space characters
                plainText += cipherChar
                continue
            # the code below is the inverse function of that used for encryption (derived using congruence)
            # it decrypts a character and concatenates it to the plain text
            plainText += letter(a_inv*(digit(cipherChar)-b) % 26)   
        return plainText



# THE TRANSPOSITION CIPHER CLASS
class TranspositionCipher:
    
    def encrypt(self, plainText: str, key: list,):
        # the key is a bijection from the set {0, 1, 2, ... n} to one of its permulations.
        # we determine the block length from the length of the key
        blockLength = len(key)
        # we pad the plainText from the right if required
        while (blockLength - len(plainText) % blockLength) % blockLength:
            plainText += letter(randint(0, 25))

        cipherText = ""
        blockStartIndex = 0
        while blockStartIndex + blockLength <= len(plainText):
            cipherBlock = ""
            block = plainText[blockStartIndex: blockStartIndex + blockLength]
            # do the encryption here
            for index in key:
                cipherBlock += block[index]
            cipherText += cipherBlock
            blockStartIndex += blockLength
        return cipherText

    def decrypt(self, cipherText: str, key: list):
        # the decryption process is identical to the encryption process. the only difference is,
        # that we use the inverse of the encryption function to make the decryption key.
        inv_key = [0 for _ in range(len(key))]
        for key_ind in key:
            inv_key[key[key_ind]] = key_ind
        # now call the encrypt method with the inverse key
        return self.encrypt(cipherText, inv_key)
            
        


# THE RSA CLASS
class RSA:
    # this RSA algorithm encrypts and decrypts letters, not text.
    def __init__(self, key: tuple, prime1:int, prime2:int):
        # the constructor takes a public key in the form of a tuple and the two primes
        # that make up the modulus. The private key is also set in the constructor.
        self.publicKey = key
        num =  inverse_mod_m(key[1], (prime1-1)*(prime2-1))
        self.privateKey = (key[0], num)


    def encrypt(self, letter):
        # to encrypt, we follo the steps mentioned in the book by raising 
        # the plain digit to the encryption number modulo m
        digit = ord(letter)
        cipherDigit = pow(digit, self.publicKey[1], self.publicKey[0])
        cipherLetter = chr(cipherDigit)
        return cipherLetter

    def decrypt(self, letter):
        # to decrypt, we raise the cipher digit by the decryption number modulo m
        cipherDigit = ord(letter)
        plainDigit = pow(cipherDigit, self.privateKey[1], self.privateKey[0])
        plainLetter = chr(plainDigit)
        return plainLetter



def main():
    if sys.argv[1] == "affine":
        # with affine, we encrypt like ... affine en secret
        # and we decrypt like ... affine de thecipher
        affine = AffineCipher()
        method, text = sys.argv[2], sys.argv[3]
        if method == "en":
            print("cipher text: ", end="")
            print(affine.encrypt(text, ((15, 21))))
        elif method == "de":
            print("plain text: ", end="")
            print(affine.decrypt(text, (15,21)))
    elif sys.argv[1] == "transposition":
        # with transposition, we encrypt like ... transposition en secret
        # and we decrypt like .... transposition de cipherText
        transposition = TranspositionCipher()
        method, text = sys.argv[2], sys.argv[3]
        if method == "en":
            print("cipher text: ", end="")
            print(transposition.encrypt(text, [2,0,3,1]))
        else:
            print("plain text: ", end="")
            print(transposition.decrypt(text, [2,0,3,1]))
    elif sys.argv[1] == "rsa":
        # with RSA, we encrypt like ... rsa en B
        # and we decrypt like .... rsa de J
        # we initialize the rsa object with some pre-defined keys
        rsa = RSA((253, 7), 11, 23)
        method, letter = sys.argv[2], sys.argv[3]
        if method == "en":
            print("cipher letter: ", end="")
            print(rsa.encrypt(letter))
        elif method == "de":
            print("plain letter: ", end="")
            print(rsa.decrypt(letter))
    else:
        print("unknown encryption")

main()