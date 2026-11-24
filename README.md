# Cryptanalysis Suite

A Python-based cryptanalysis suite implementing classical and modern cryptanalytic attacks. This repository contains scripts and writeups for breaking a weak-key AES-128 and monoalphabetic substitution scheme, demonstrating one-time pad key ambiguity (perfect secrecy), and executing a known-plaintext attack against a repeating-key XOR stream cipher.

---

## 📁 Repository Structure

```text
cryptanalysis-suite/
├── task01/
│   ├── aes.key                      # Recovered 128-bit AES key (hex string, 16-bit weak key + zero padding)
│   ├── subst.key                    # Recovered monoalphabetic substitution key (plain -> cipher)
│   ├── bruteforce_aes.py            # AES-128-CBC weak-key brute-force script
│   ├── break_monoalphabetic.py      # Hill-climbing monoalphabetic cipher solver
│   ├── ngram_score.py               # Quadgram frequency scoring module
│   ├── english_quadgrams.txt        # Reference English quadgram dataset
│   ├── Subst-Rijndael.crypt         # Double-encrypted input binary (Substitution then AES-128-CBC)
│   ├── Subst.txt                    # Intermediate AES-decrypted substitution ciphertext
│   └── decrypted.txt                # Final recovered plaintext
│
├── task02/
│   ├── k1.key                       # Derived 40-byte binary OTP key for Plaintext 1
│   ├── k2.key                       # Derived 40-byte binary OTP key for Plaintext 2
│   ├── cipher_keys.py               # One-time pad (XOR) dual-key derivation script
│   ├── cipher.crypt                 # 40-byte ciphertext binary file
│   ├── plaintext1.txt               # Candidate message 1 (40 bytes)
│   ├── plaintext2.txt               # Candidate message 2 (40 bytes)
│   └── writeup.md                   # One-time pad analysis and writeup
│
└── task03/
    ├── XOR.key                      # Recovered 96-bit (12-byte) XOR key (hex string)
    ├── XOR_decrypter.py             # Known-plaintext repeating-XOR decryptor
    ├── XOR.zip.crypt                # Encrypted ZIP archive
    ├── decrypted.zip                # Recovered ZIP archive
    └── writeup.md                   # Cryptanalysis methodology and writeup
```

---

## 🔐 Overview of Tasks & Features

### 1. Task 01: Ciphertext-Only Analysis (AES-128 & Hill-Climbing)
Analyzes and breaks a two-layer encryption scheme (`Monoalphabetic Substitution` $\rightarrow$ `AES-128-CBC`), decrypted in reverse (`AES-128-CBC` $\rightarrow$ `Monoalphabetic Substitution`).

* **Part A: AES-128 Weak Key Brute-Force (`bruteforce_aes.py`)**
  * Attacks a reduced key-space AES-128-CBC cipher where only the first 16 bits are unknown and the remaining 112 bits are zero-padded.
  * Reads the 16-byte IV from the first block of `Subst-Rijndael.crypt` and uses Shannon entropy scoring to identify the valid key among all $65,536$ candidates without requiring known plaintext.
  * Writes the recovered hex key to `aes.key` and saves the space-stripped intermediate ciphertext to `Subst.txt`.

* **Part B: Hill-Climbing Substitution Solver (`break_monoalphabetic.py`)**
  * Solves the inner monoalphabetic substitution cipher ($26! \approx 4 \times 10^{26}$ search space).
  * Initializes the 26-letter substitution mapping using letter frequency analysis.
  * Runs iterative hill-climbing with random letter swaps (plus 20 restarts with 3-swap perturbations) scored by English quadgram log-probabilities (`ngram_score.py`), saving the inverted `plain -> cipher` key to `subst.key` and the plaintext to `decrypted.txt`.

### 2. Task 02: One-Time Pad & Key Ambiguity (`task02/`)
Demonstrates perfect secrecy using a bitwise XOR one-time pad (`Enc_k(p) = p XOR k`), showing that a single 40-byte ciphertext (`cipher.crypt`) can decrypt to two completely different, meaningful 40-byte plaintexts (`plaintext1.txt` and `plaintext2.txt`) depending on which key (`k1.key` or `k2.key`) is supplied.

* `cipher_keys.py`: Derives `k1 = c XOR p1` and `k2 = c XOR p2`, verifies decryption back to both messages, and writes the binary keys to `k1.key` and `k2.key`.
* `writeup.md`: Explains the XOR key derivation and why a truly random, single-use, message-length key provides perfect secrecy.

### 3. Task 03: Known-Plaintext XOR Attack (`task03/`)
Mounts a known-plaintext attack (KPA) against an encrypted ZIP archive (`XOR.zip.crypt`) encrypted with a repeating 96-bit (12-byte) XOR key.

* **Methodology (`XOR_decrypter.py`)**:
  * Uses fixed structural bytes from the ZIP file format specification: the local file header signature (`PK\x03\x04` at offset `0`), the End of Central Directory signature and zeroed disk fields (`PK\x05\x06` + 4 zero bytes at `n - 22`), and the 2-byte zero comment length at `n - 2`.
  * Recovers all 12 key bytes via `key[i % 12] = cipher[i] ^ plain[i]`.
  * Decrypts `XOR.zip.crypt` into a valid archive (`decrypted.zip`) and writes the hex-encoded key to `XOR.key`.

---

## 🚀 Quick Start & Usage

### Prerequisites
* Python 3.x
* `pycryptodome` (required only for `task01/bruteforce_aes.py`)

```bash
pip install pycryptodome
```

> **Note:** Running any of the scripts below overwrites the existing `.key`, `Subst.txt`, `decrypted.txt`, and `decrypted.zip` output files in that task's directory.

### Running Task 01
```bash
cd task01
# Step 1: Brute-force weak AES key
python bruteforce_aes.py

# Step 2: Break monoalphabetic substitution via hill climbing
python break_monoalphabetic.py
```

### Running Task 02
```bash
cd task02
python cipher_keys.py
```

### Running Task 03
```bash
cd task03
python XOR_decrypter.py
```

---

## 📜 License
Distributed under the MIT License.
