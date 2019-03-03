import random

'''
Euclid's algorithm for determining the greatest common divisor
Use iteration to make it faster for larger integers
'''


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


'''
Euclid's extended algorithm for finding the multiplicative inverse of two numbers
'''

'''
def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi / e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi

'''


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def multiplicative_inverse(e, phi):
    g, x, y = egcd(e, phi)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % phi


'''
Tests to see if a number is prime.
'''


def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(pow(num, 0.5)) + 2, 2):
        if num % n == 0:
            return False
    return True


def generate_keypair(P, Q):
    if not (is_prime(P) and is_prime(Q)):
        raise ValueError('Both numbers must be prime.')
    elif P == Q:
        raise ValueError('p and q cannot be equal')
    # n = pq
    n = P * Q

    # Phi is the Totient of n
    phi = (P - 1) * (Q - 1)

    # Choose an integer e such that e and phi(n) are co-prime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are co-prime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)

    # Return public and private key pair
    # Public key is (e, n) and private key is (d, n)
    return (e, n), (d, n)


def encrypt(pk, plaintext):
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [(pow(ord(char), key, n)) for char in plaintext]
    # Return the array of bytes
    return cipher


def decrypt(pk, ciphertext):
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr(pow(char, key) % n) for char in ciphertext]
    # Return the array of bytes as a string
    return ''.join(plain)


def s2l(msg):
    msg = msg.strip("[")
    msg = msg.strip("]")
    msg = msg.split(", ")
    lm = len(msg)
    lstm = [0] * lm
    for i in range(0, lm):
        lstm[i] = int(msg[i])
    return lstm


if __name__ == '__main__':
    '''
    Detect if the script is being run directly by the user
    '''
    print("RSA Encrypter/ Decrypter")
    p = int(input("Enter a prime number (17, 19, 23, etc): "))
    q = int(input("Enter another prime number (Not one you entered above): "))
    print("Generating your public/private key pairs now . . .")

    public, private = generate_keypair(p, q)
    print("Your public key is ", public, " and your private key is ", private)
    message = input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(private, message)
    print("Your encrypted message is: ")
    print(''.join(map(lambda x: str(x), encrypted_msg)))
    print("Decrypting message with public key ", public, " . . .")
    print("Your message is:")
    print(decrypt(public, encrypted_msg))
