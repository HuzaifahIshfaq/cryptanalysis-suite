## Idea:
 The file is a ZIP encrypted with a repeating 12-byte XOR key, so byte `i` is XORed with `key[i mod 12]`. Known plaintext reveals the key: `key[i mod 12] = cipher[i] XOR plain[i]`.

## Known plaintext (ZIP format):
- File start: `50 4B 03 04` gives key bytes 0-3.
- End of central directory record (22 bytes): `50 4B 05 06 00 00 00 00` gives key bytes 3-10.
- Last two bytes (comment length `00 00`) give key bytes 11 and 0.

## Result:
 Key (hex): `6c5ed0703435e77ff6749190`. XORing the file with this key gives a valid ZIP, from which `readme file` could be extracted.

## Why it works:
 A short key repeated over the whole file, so a few known bytes are enough to recover it.
