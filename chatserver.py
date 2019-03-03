import socket

from rsa import *

print("\nCryptography Chatting Room\n")

s = socket.socket()
host = socket.gethostname()
ip = socket.gethostbyname(host)
port = 1234
s.bind((host, port))
print(host, "(", ip, ")\n")


s.listen(1)
print("\nWaiting for incoming connections...\n")
conn, addr = s.accept()
print("Received connection from ", addr[0], "(", addr[1], ")\n")
print("Client Connected to the chat room\nEnter 'e' to exit chat room\n")

p = int(input("Enter A Large Prime Number: "))
q = int(input("Enter A Large Prime Number (Not same as ALREADY ENTERED!!): "))
public, private = generate_keypair(p, q)
print("Your public key is ", public, " and your private key is ", private)
pub0 = str(public[0])
conn.send(pub0.encode())
pub1 = str(public[1])
conn.send(pub1.encode())
cpub0 = conn.recv(1024)
cpub0 = int(cpub0.decode())
cpub1 = conn.recv(1024)
cpub1 = int(cpub1.decode())
cpub = (cpub0, cpub1)
print("Shared Public Key Is: ", cpub)

while True:
    # Encrypting Message
    print("Enter 1 to Encrypt with Public Key")
    print("Enter 2 to Encrypt with Private Key")
    print("Enter 3 to Encrypt with Digital Signature")
    eop = int(input("Your Option: "))

    # Using Sender's Public Key To Encrypt
    if eop == 1:
        message = input(str("Me : "))
        bye = message
        if message == 'e':
            message = "Left chat room!"
        enc = encrypt(cpub, message)
        print("Encryted Message: ", ''.join(map(lambda z: str(z), enc)))
        enc = str(enc)
        conn.send(enc.encode())
        if bye == "[e]":
            print("You Left The Chat Room!!\n")
            break

    # Using Private Key To Encrypt
    elif eop == 2:
        message = input(str("Me : "))
        bye = message
        if message == 'e':
            message = "Left chat room!"
        enc = encrypt(private, message)
        print("Encryted Message: ", ''.join(map(lambda z: str(z), enc)))
        enc = str(enc)
        conn.send(enc.encode())
        if bye == 'e':
            print("You Left The Chat Room!!\n")
            break

    # Using Both Keys to Encrypt
    elif eop == 3:
        message = input(str("Me : "))
        bye = message
        if message == 'e':
            message = "Left chat room!"
        sgn = encrypt(private, message)
        print("Encryption With Private Key: ", ''.join(map(lambda z: str(z), sgn)))
        sgn = str(sgn)
        enc = encrypt(cpub, sgn)
        enc = str(enc)
        lstm = s2l(enc)
        print("Encrypted Message: ", ''.join(map(lambda z: str(z), lstm)))
        conn.send(enc.encode())
        if bye == 'e':
            print("You Left The Chat Room!!\n")
            break

    # Decrypting Message
    message = conn.recv(1024)
    message = message.decode()
    lstm = s2l(message)
    print("Client", ":", ''.join(map(lambda z: str(z), lstm)))
    print("Enter 1 to Decrypt using Public Key")
    print("Enter 2 to Decrypt using Private Key")
    print("Enter 3 to Decrypt using Both Keys")
    dop = int(input("Your Option: "))

    # Using Sender's Public Key To Decrypt
    if dop == 1:
        dec = decrypt(cpub, lstm)
        print("Decrypted Message: ", dec)

    # Using Private Key To Decrypt
    elif dop == 2:
        dec = decrypt(private, lstm)
        print("Decrypted Message: ", dec)

    # Using Both Keys to Decrypt
    elif dop == 3:
        dec = decrypt(private, lstm)
        lstm = s2l(dec)
        dec = decrypt(cpub, lstm)
        print("Decrypted Message: ", dec)
