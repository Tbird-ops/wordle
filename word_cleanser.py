# Tbird's dictionary creator
# I needed something to go from a dirty wordlist, aka possible submittables to wordle,
# but not solutions, down to a list of defineable true english words. 
# Found the PyEnchant library could give a boolean value of whether or not a word
# was defineable and therefore a true word string.
#
# My first megawordlist was 19183 words long. After running this, my dictionary was only 6452
# I presume this will have significant improvements on my apps predictions.

import enchant

d = enchant.Dict("en_US")

cleansed = []

print("Beginning filter: ", end="")
# with open("mega_list_full.txt", "r") as original:
with open("old_wordlists_trashbin/mega_list_full.txt", "r") as original:
    for line in original:
        if len(line.replace("\n", "")) == 5:
            if d.check(line.replace("\n", "")) and line.lower() not in cleansed:
                cleansed.append(line.lower())
print("DONE")

good = {}

print("Collecting wordle words: ", end='')
with open("tests/wordle_possible_submittables") as approved:
    for line in approved:
        good[line.lower()] = 0
print("DONE")

print("Wordlable: ", end="")
for word in cleansed:
    try:
        good[word.lower()] = 1
    except KeyError:
        continue
print("DONE")

wordleable = [k for k, v in good.items() if v == 1]

print("Beginning write: ", end="")
with open("dictionary.txt", "w") as good_things:
    good_things.writelines(wordleable)
print("DONE")

