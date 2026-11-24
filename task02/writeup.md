## Algorithm
One-time pad: bitwise XOR of the plaintext with a key of the same length.
Enc_k(p) = p XOR k, Dec_k(c) = c XOR k.

## Approach
cipher.crypt, plaintext1.txt and plaintext2.txt all have the same length (40 bytes).
Since c = p XOR k, the key for a desired plaintext is k = c XOR p.
So I computed k1 = c XOR p1 and k2 = c XOR p2 (script: cipher_keys.py).
Decrypting c with k1 gives plaintext 1, and decrypting c with k2 gives plaintext 2.

## Why this works
For any plaintext of the right length there is a key that maps the ciphertext to it.
Therefore the ciphertext alone gives no information about which message is real.
This is perfect secrecy. It only holds if the key is random, as long as
the message, and used once.

I also did this task on Cryptool 2.1 but i choose this python script as my submission. During lab defence i can also show how i did that if requested.