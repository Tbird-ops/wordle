# Used to build a bit of a weight towards words with more common letters
# This was my first idea that came to mine. Probably not the most efficient,
# but I was curious how well it worked!

import heapq as hq

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

#* Generate Word weights
# Using a set method in order to maximize first guess information
# Without sets, the theoretical best word my wordlist would use was "Eerie" (note the number of 'e's)
# With sets, the new best was "Irate", a much better improvement over "eerie". Uses many of the top letters
#! for the heap to work, needed to multiply the weight by -1 to get a max heap to work as a min heap
def gen_wordlist():
    word_weights = {}
    with open("5letterwords", "r") as words:
        for line in words.readlines():
            word = line.lower()[:-1]
            weight = 0
            try: 
                for letter in set(word):
                    weight += frequencies[letter]
                word_weights[line] = weight * -1 # for the heaping
            # Protect from failure of "dirty" wordlists (punctuation, accented characters,etc)
            except KeyError:
                continue
    return [(word_weights[key], key) for key in word_weights]

#* Print the best guesses given the current information.
# Made into a heap so that I could just use the pop function to sort the guess ranking.
#
# OLD METHOD
# N = 10
# for _ in range(N):
#     heighest_word = None
#     tmp = 0
#     for key in word_weights:
#         if word_weights[key] > tmp and key not in topN:
#             tmp = word_weights[key]
#             heighest_word = key
#     topN.append(heighest_word)

#? moved to main file?
# def heapit(word_weights)
#     return hq.heapify(word_weights)