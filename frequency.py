# Used to build a bit of a weight towards words with more common letters
# This was my first idea that came to mine. Probably not the most efficient,
# but I was curious how well it worked!

# Pulled from https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html
frequencies = {
    "e": 11.1607,
    "a": 8.4966,
    "r": 7.5809,
    "i": 7.5448,
    "o": 7.1635,
    "t": 6.9509,
    "n": 6.6544,
    "s": 5.7351,
    "l": 5.4893,
    "c": 4.5388,
    "u": 3.6308,
    "d": 3.3844,
    "p": 3.1671,
    "m": 3.0129,
    "h": 3.0034,
    "g": 2.4705,
    "b": 2.0720,
    "f": 1.8121,
    "y": 1.7779,
    "w": 1.2899,
    "k": 1.1016,
    "v": 1.0074,
    "x": 0.2902,
    "z": 0.2722,
    "j": 0.1965,
    "q": 0.1962,
}

def generate_freq():
    generated = {}
    count = 0

    with open("dictionary.txt", "r") as words:
        for word in words:
            # DEBUG
            # if count % 100 == 0:
            #     print(word.replace('\n', ''))
            for letter in word.replace('\n', '').lower():
                count += 1
                if letter not in generated.keys():
                    generated[letter] = 1
                else:
                    generated[letter] += 1

    for letter in generated.keys():
        generated[letter] = generated[letter] / count * 100
    return generated

def combine(oldfreq, newfreq):
    combined = []
    for i in range(len(oldfreq)):
        letter = chr(ord('a') + i)
        old = oldfreq[letter]
        new = newfreq[letter]
        combined.append((letter, old, new))
    return combined