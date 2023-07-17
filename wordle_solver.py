# Tbird's wordle solver!
# This idea came to me one night playing wordle and using regex against the oxford dictionary lol

# Used to build a bit of a weight towards words with more common letters
# This was my first idea that came to mine. Probably not the most efficient,
# but I was curious how well it worked!

import re  # gotta have regex ;)
from os import system # to clear screen

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

# This defines the current known word letters. Is filled in by the "regexr"
word_match = ["." for i in range(5)]
search_string = "^"

#* Generate Word weights
# Using a set method in order to maximize first guess information
# Without sets, the theoretical best word my wordlist would use was "Eerie" (note the number of 'e's)
# With sets, the new best was "Irate", a much better improvement over "eerie". Uses many of the top letters
# Wordlist is custom created from a copy of the Oxford dictionary I downloaded and regexed a bit to get unique, mostly cleaned 5 letter words
def gen_wordlist():
    word_weights = {}
    with open("bigwordlist", "r") as words:
        for line in words.readlines():
            word = line.lower().replace("\n", "")
            weight = 0
            try: 
                for letter in set(word):
                    weight += frequencies[letter]
                word_weights[word] = weight
            # Protect from failure of "dirty" wordlists (punctuation, accented characters,etc)
            except KeyError:
                continue
    return sorted([(word_weights[key], key) for key in word_weights], reverse=True)

#* Make best guess
def guesser(weighted_wordlist):
    return weighted_wordlist.pop(0)

#* Build new regex expression
def regexr(good=[], bad=[], exact=[]):
    global search_string
    global word_match

    match_string = search_string
    if '' not in good:
        for letter in good:
            match_string += f'(?=.*{letter})'
    if '' not in bad:
        for letter in bad:
            match_string += f'(?!.*{letter})'
    search_string = match_string
    if '' not in exact:
        for letter in exact:
            loc,let = letter.split(":")
            word_match[int(loc)-1] = let
    match_string += ''.join(word_match)

    ##? DEBUG
    # print(match_string)
    
    return match_string

#* Ask about current status
def questionaire():
    win = input("Did we win? (y/n) > ")[0].lower()
    if win == "n":
        good = input("What letters are YELLOW? (multiple letters separate by commas. ie 'a, e, f')\n> ").replace(" ", "").lower().split(",")
        bad = input("What letters are GRAY? (multiple letters separate by commas. ie 'a, e, f')\n> ").replace(" ","").lower().split(",")
        exact = input("What letters are GREEN? (give answers in N:L format. multiple comma separated\n> ").replace(" ","").lower().split(",")
        return good, bad, exact
    else:
        print("Yay!")
        exit(0)

#* Cut out words that don't match
def sifter(comparison, weighted_wordlist):
    new_list = []
    for _ in range(len(weighted_wordlist)):
        tmp = weighted_wordlist.pop(0)
        ##? DEBUG
        # print(f"Checking {tmp[1]}... ", end="")
        if re.match(comparison, tmp[1]) != None:
            new_list.append(tmp)
            ##? DEBUG
            # print(f"appending! {tmp[1]}")
        ##? DEBUG
        # else:
        #     print()
            
    return new_list

def run_test():
    global word_match
    global search_string
    wins = 0
    games = 0
    tries = 0
    distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    with open("wordlelist1", "r") as game:
        for line in game.readlines():
            # New game for gamecount
            games += 1
            
            # Pick next word and strip newline
            answer = line.lower().replace("\n", "")

            if games % 100 == 0:
                print(f'Current word: {answer}')

            # Start my wordler
            words = gen_wordlist()
            search_string = "^"
            word_match = ["." for i in range(5)]
            for attempts in range(6):
                tries += 1
                guess = guesser(words)[1]
                if guess == answer:
                    wins += 1
                    distribution[attempts+1] += 1
                    break
                else:
                    good = []
                    bad = []
                    exact = []
                    index = 0
                    for letter in guess:
                        if letter in answer:
                            if letter == answer[index]:
                                exact.append(f'{index+1}:{letter}')
                            else:
                                good.append(letter)
                        else:
                            bad.append(letter)
                        index += 1
                comparison = re.compile(regexr(good, bad, exact))
                words = sifter(comparison, words)
    
    print(f'Wins: {wins}')
    print(f'Losses: {games-wins}')
    print(f'Avg: {wins/games}')
    print(f'Distribution: 1:{distribution[1]}  2:{distribution[2]}  3:{distribution[3]}  4:{distribution[4]}  5:{distribution[5]}  6:{distribution[6]}')
    print(f'Games played: {games}')


def main(test=0):
    if test == 1:
        run_test()
    else:
        # Initiate the wordler
        words = gen_wordlist()
        guess = guesser(words)
        print("Tbird's Wordler!")
        print(f"Here is the best guess to start '{guess[1]}'\n")
        
        # Learn for next round
        for _ in range(5):
            good, bad, exact = questionaire()
            comparison = re.compile(regexr(good, bad, exact))
            words = sifter(comparison, words)
            ##? DEBUG
            # print(words)
            guess = guesser(words)
            print(f"New best guess: '{guess[1]}'\n")

if __name__ == "__main__":
    # main(test=1)
    main()
