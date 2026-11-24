
c = open("XOR.zip.crypt", "rb").read()
n = len(c)            # file length
key = [None] * 12     # 96-bit key = 12 bytes, 12 slots for key bytes

def learn(pos, plain):
  
    for off, p in enumerate(plain):
        idx = (pos + off) % 12     #finds the position of plaintext and works out which key slot it belongs to
        kb = c[pos + off] ^ p      #finds the key byte by XORing cipher with plain
        if key[idx] is None:
            key[idx] = kb
        elif key[idx] != kb:
            print("CONFLICT at key index", idx)     #gives and error if the key slot is already filled

# Known plaintext, fixed by the ZIP format:
learn(0, b"PK\x03\x04")                      # start: local file header signature -> key bytes 0-3
learn(n - 22, b"PK\x05\x06" + bytes(4))      # end record (22 bytes): signature + zero disk fields -> key bytes 3-10
learn(n - 2, bytes(2))                       # last 2 bytes: comment length = 0 -> key bytes 11 and 0


# decrypting by XORing every byte with its key byte
k = bytes(key)
plain = bytes(b ^ k[i % 12] for i, b in enumerate(c))

# save the decrypted ZIP and the key as a hex string
open("decrypted.zip", "wb").write(plain)
open("XOR.key", "w").write(k.hex())
print("key hex:", k.hex())