# Cryptanalysis Suite

A Python-based cryptanalysis suite implementing classical and modern cryptanalytic attacks. This repository contains custom scripts, tools, and writeups for breaking weak encryption schemes, performing heuristic substitution analysis, analyzing multi-key ciphers, and executing known-plaintext stream cipher attacks.

---

## 📁 Repository Structure

```text
cryptanalysis-suite/
├── task01/
│   ├── aes.key                      # Recovered 16-bit AES key (hex string)
│   ├── subst.key                    # Recovered monoalphabetic substitution key
│   ├── bruteforce_aes.py            # AES-128 weak-key brute-force script
│   ├── break_monoalphabetic.py      # Hill-climbing monoalphabetic cipher solver
│   ├── ngram_score.py               # Quadgram frequency scoring module
│   ├── english_quadgrams.txt        # Reference English quadgram dataset
│   ├── Subst-Rijndael.crypt         # Double-encrypted input binary (AES + Substitution)
│   ├── Subst.txt                    # Intermediary AES-decrypted text
│   └── decrypted.txt                # Final fully decrypted plaintext
│
├── task02/
│   ├── k1.key                       # Recovered key for Plaintext 1
│   ├── k2.key                       # Recovered key for Plaintext 2
│   ├── cipher_keys.py               # Dual-key encryption/decryption algorithm script
│   ├── cipher.crypt                 # Ciphertext binary file
│   ├── plaintext1.txt               # Opposing candidate message 1
│   ├── plaintext2.txt               # Opposing candidate message 2
│   └── writeup.md                   # Algorithm breakdown and technical writeup
│
└── task03/
    ├── XOR.key                      # Recovered 96-bit (12-byte) XOR key (hex string)
    ├── XOR_decrypter.py             # Known-plaintext XOR stream decryptor
    ├── XOR.zip.crypt                # Encrypted ZIP file
    ├── decrypted.zip                # Successfully recovered ZIP archive
    └── writeup.md                   # Cryptanalysis methodology and writeup
```

---

## 🔐 Overview of Tasks & Features

### 1. Task 01: Ciphertext-Only Analysis (AES-128 & Hill-Climbing)
Analyzes and breaks a two-layer encryption scheme (`AES-CBC` $\rightarrow$ `Monoalphabetic Substitution`).

* **Part A: AES-128 Weak Key Brute-Force (`bruteforce_aes.py`)**
  * Attacks a reduced key-space AES-128 cipher where only the first 16 bits are unknown and the remaining 112 bits are zero-padded.
  * Uses Shannon entropy scoring to automatically identify the valid key among all $65,536$ candidates without requiring known plaintext.
  * Outputs the recovered AES key to `aes.key` and saves the intermediate ciphertext to `Subst.txt`.

* **Part B: Hill-Climbing Substitution Solver (`break_monoalphabetic.py`)**
  * Solves the inner monoalphabetic substitution cipher ($26! \approx 4 \times 10^{26}$ search space).
  * Automatically initializes the substitution matrix using letter frequency analysis.
  * Uses an iterative hill-climbing algorithm with random key transpositions and English quadgram fitness scoring (`ngram_score.py`) to converge on the optimal key table (`subst.key`) and output `decrypted.txt`.

### 2. Task 02: Dual-Key Algorithm Construction (`task02/`)
Investigates cipher construction where a single ciphertext (`cipher.crypt`) can be validly decrypted into two entirely different, meaningful plaintexts (`plaintext1.txt` and `plaintext2.txt`) depending on which key (`k1.key` or `k2.key`) is supplied.

* `cipher_keys.py`: Re-creates the encryption/decryption function mapping both keys to the target ciphertext.
* `writeup.md`: Details the structural properties and mathematical foundations behind the underlying cipher scheme.

### 3. Task 03: Partial Known-Plaintext Analysis (`task03/`)
Mounts a known-plaintext attack (KPA) against an encrypted ZIP archive (`XOR.zip.crypt`) encrypted with a 96-bit (12-byte) repeating XOR key.

* **Methodology (`XOR_decrypter.py`)**:
  * Leverages predictable structural headers inherent to the standard ZIP file format specification (PK zip headers).
  * Recovers the 12-byte key stream by XORing target header bytes with the known binary signatures.
  * Decrypts `XOR.zip.crypt` into a valid archive (`decrypted.zip`) and extracts `XOR.key`.

---

## 🚀 Quick Start & Usage

### Prerequisites
* Python 3.x
* `pycryptodome` (for AES decryption routines)

```bash
pip install pycryptodome
```

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
Distributed under the MIT License. See `LICENSE` for more information.