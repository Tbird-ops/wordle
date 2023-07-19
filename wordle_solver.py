# Tbird's wordle solver!
# This idea came to me one night playing wordle and using regex against the oxford dictionary lol

# Used to build a bit of a weight towards words with more common letters
# This was my first idea that came to mine. Probably not the most efficient,
# but I was curious how well it worked!

import re  # gotta have regex ;)
import frequency

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
    with open("dictionary.txt", "r") as words:
        for line in words.readlines():
            word = line.lower().replace("\n", "")
            weight = 0
            try: 
                for letter in set(word):
                    weight += frequency.frequencies[letter]
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

    with open("tests/wordle_old_solutions", "r") as game:
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
                try:
                    guess = guesser(words)[1]
                # TODO build this out to understand why it failed to guess
                # TODO REMOVE 'ELMER' from wordlist
                except IndexError:
                    break
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
        # TODO until my guesser gets better, need more attempts than 6 due to some word failures
        while True:
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
