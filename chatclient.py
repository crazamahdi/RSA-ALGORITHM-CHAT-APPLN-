import socket

from rsa import *

print("\nWelcome to Chat Room\n")

s = socket.socket()
shost = socket.gethostname()
ip = socket.gethostbyname(shost)
print(shost, "(", ip, ")\n")
host = 'localhost'
port = 1234
s.connect((ip, port))
print("Connected...\n")


print("Joined the chat room\nEnter [e] to exit chat room\n")

p = int(input("Enter A Large Prime Number: "))
q = int(input("Enter A Large Prime Number (Not same as ALREADY ENTERED!!): "))
public, private = generate_keypair(p, q)
print("Your public key is ", public, " and your private key is ", private)
spub0 = s.recv(1024)
spub0 = int(spub0.decode())
spub1 = s.recv(1024)
spub1 = int(spub1.decode())
spub = (spub0, spub1)
pub0 = str(public[0])
s.send(pub0.encode())
pub1 = str(public[1])
s.send(pub1.encode())
print("Shared Public Key: ", spub)

while True:

    # Decrypting Message
    message = s.recv(1024)
    message = message.decode()
    lstm = s2l(message)
    print("Server", ":", ''.join(map(lambda z: str(z), lstm)))
    print("Enter 1 to Decrypt with Public Key")
    print("Enter 2 to Decrypt with Private Key")
    print("Enter 3 to Decrypt with Digital Signature")
    dop = int(input("Your Option: "))

    # Using Sender's Public Key To Decrypt
    if dop == 1:
        dec = decrypt(spub, lstm)
        print("Decrypted Message: ", dec)

    # Using Private Key To Decrypt
    elif dop == 2:
        dec = decrypt(private, lstm)
        print("Decrypted Message: ", dec)

    # Using Both Keys to Decrypt
    elif dop == 3:
        dec = decrypt(private, lstm)
        lstm = s2l(dec)
        dec = decrypt(spub, lstm)
        print("Decrypted Message: ", dec)

    # Encrypting Message
    print("Enter 1 to Encrypt with Public Key")
    print("Enter 2 to Encrypt with Private Key")
    print("Enter 3 to Encrypt with Digital Signature")
    eop = int(input("Your Option: "))

    # Using Sender's Public Key To Encrypt
    if eop == 1:
        message = input(str("Me : "))
        bye = message
        if message == "[e]":
            message = "Left chat room!"
        enc = encrypt(spub, message)
        print("Encrypted Message: ", ''.join(map(lambda z: str(z), enc)))
        enc = str(enc)
        s.send(enc.encode())
        if bye == "[e]":
            print("You Left chat room!")
            print("\n")
            break

    # Using Private Key To Encrypt
    elif eop == 2:
        message = input(str("Me : "))
        bye = message
        if message == "[e]":
            message = "Left chat room!"
        enc = encrypt(private, message)
        print("Encrypted Message: ", ''.join(map(lambda z: str(z), enc)))
        enc = str(enc)
        s.send(enc.encode())
        if bye == "[e]":
            print("You Left chat room!")
            print("\n")
            break

    # Using Both Keys to Encrypt
    elif eop == 3:
        message = input(str("Me : "))
        bye = message
        if message == "[e]":
            message = "Left chat room!"
        sgn = encrypt(private, message)
        print("Encryption With Private Key: ", ''.join(map(lambda z: str(z), sgn)))
        sgn = str(sgn)
        enc = encrypt(spub, sgn)
        enc = str(enc)
        lstm = s2l(enc)
        print("Encrypted Message: ", ''.join(map(lambda z: str(z), lstm)))
        s.send(enc.encode())
        if bye == "[e]":
            print("You Left The Chat Room!!\n")
            break
