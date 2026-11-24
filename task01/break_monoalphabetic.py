import random
from collections import Counter
from ngram_score import ngram_score   

ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ENGLISH_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"   # English letters, most to least frequent
NGRAM_FILE = "english_quadgrams.txt"           # quadgram statistics used by the scorer

# fitness.score(text) rates how English-like a text is (higher = better)
fitness = ngram_score(NGRAM_FILE)


def decrypt(text, key):
    # it takes the gussed key and and turns the cipher into plaintext.
    return text.translate(str.maketrans(ALPHA, key))


def init_key(cipher):
    # Starting guess from frequency analysis:
    counts = Counter(c for c in cipher if c in ALPHA)
    by_freq = sorted(ALPHA, key=lambda c: -counts[c])   # cipher letters, most common first
    key = [""] * 26
    for cipher_letter, plain_letter in zip(by_freq, ENGLISH_ORDER):
        key[ALPHA.index(cipher_letter)] = plain_letter
    return "".join(key)


def hill_climb(letters, key, max_stall=2000):
    best = fitness.score(decrypt(letters, key))   # score of the starting key
    stall = 0                                     # failed attempts in a row
    while stall < max_stall:
        # Next key: swap two random letters of the key (one transposition)
        i, j = random.sample(range(26), 2)
        k = list(key)
        k[i], k[j] = k[j], k[i]
        cand = "".join(k)

        # Keep the swap only if the decryption looks more like English
        s = fitness.score(decrypt(letters, cand))
        if s > best:
            key, best, stall = cand, s, 0
        else:
            stall += 1
    # No swap has helped for max_stall tries in a row: stop
    return key, best


def main():
    with open("Subst.txt") as f:
        cipher = f.read().upper()
    # Only the letters A-Z are scored; the full text is kept for the readable preview
    letters = "".join(c for c in cipher if c in ALPHA)

    # First run: start from the frequency-based key and climb
    best_key, best_score = hill_climb(letters, init_key(cipher))
    print("first run score:", round(best_score, 1))

    # Restarts: climbing can get stuck on a local maximum, so shake the best key
    # with 3 random swaps and climb again. Keep the result if it is better.
    for r in range(20):
        k = list(best_key)
        for _ in range(3):
            i, j = random.sample(range(26), 2)
            k[i], k[j] = k[j], k[i]
        key, score = hill_climb(letters, "".join(k))
        if score > best_score:
            best_key, best_score = key, score
            print(f"restart {r}: new best score {score:.1f}")

    # Check by eye: this should be readable English
    print("\n" + decrypt(cipher, best_key)[:400])

    # best_key maps cipher -> plain, but subst.key must map plain -> cipher
    # ("plain A was mapped to ..."), so invert it
    subst_key = "".join(ALPHA[best_key.index(p)] for p in ALPHA)
    print("\nsubst.key:", subst_key)
    with open("subst.key", "w") as f:
        f.write(subst_key)
    plain = decrypt(cipher, best_key)
    with open("decrypted.txt", "w") as f:
        f.write(plain)

if __name__ == "__main__":
    main()