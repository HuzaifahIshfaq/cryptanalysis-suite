# pip install pycryptodome
from Crypto.Cipher import AES
import math
from collections import Counter


def entropy(data):
    counts = Counter(data)
    n = len(data)
    return -sum(c / n * math.log2(c / n) for c in counts.values()) # Shannon entropy function to score how random looking the data is.

with open("Subst-Rijndael.crypt", "rb") as f:
    blob = f.read()

iv = blob[:16]   # the IV is the first block (not secret)
ct = blob[16:]   # the rest is the encrypted message

results = []

# only the first 16 bits of the key are free, so there are only 2^16 = 65536 keys

for i in range(65536):
    key = bytes([i >> 8, i & 0xFF]) + bytes(14)   # 2 free bytes + 14 zero bytes
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = cipher.decrypt(ct)
    # a wrong key gives no error just garbage which would be incorrect, so we score every result by entropy
    results.append((entropy(pt), key, pt))

# wrong key will have random-looking output and entropy will be high
# right key: text like output entropy will be low
results.sort(key=lambda r: r[0])

print("lowest 5 entropies:")
for e, key, pt in results[:5]:
    print(f"  key={key.hex()}  entropy={e:.3f}")

best_e, best_key, best_pt = results[0]
print("\nbest key:", best_key.hex())
print("first 100 bytes:", best_pt[:100])   

# the last block was filled up with spaces, so remove them
text = best_pt.rstrip(b" ")

with open("aes.key", "w") as f:
    f.write(best_key.hex())   
with open("Subst.txt", "wb") as f:
    f.write(text)              