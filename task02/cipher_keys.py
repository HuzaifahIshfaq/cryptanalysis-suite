# Task 2: one-time pad (XOR) with two keys for one ciphertext
c  = open("cipher.crypt", "rb").read()
p1 = open("plaintext1.txt", "rb").read()
p2 = open("plaintext2.txt", "rb").read()
assert len(c) == len(p1) == len(p2)

def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

# c = p XOR k  ->  k = c XOR p
k1 = xor(c, p1)
k2 = xor(c, p2)

# check: decrypting c with each key gives the right message
assert xor(c, k1) == p1
assert xor(c, k2) == p2

# the sheet wants the keys as binary data
with open("k1.key", "wb") as f:
    f.write(k1)
with open("k2.key", "wb") as f:
    f.write(k2)

print("k1:", k1.hex())
print("k2:", k2.hex())
print(xor(c, k1))
print(xor(c, k2))