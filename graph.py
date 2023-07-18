# Wanted a way to see the increase/decrease of a letter's weight
# given different sets of generated frequencies.
# The `frequency.py` file is used to build a new generation of letter frequency given different dictionary.txt files

import numpy as np
import matplotlib.pyplot as plt
import frequency

# Make a list of tuples (letter, old_frequency, new_frequency)
combined = frequency.combine(frequency.frequencies, frequency.generate_freq())

# Set up bar graph structure
bar_width = 0.25
fig = plt.subplots(figsize=(12,8))

# Determine widths of bars
br1 = np.arange(len(combined))
br2 = [x + bar_width for x in br1]

# Build arrangement
plt.bar(br1, [combined[i][1] for i in range(len(combined))], color='b', width= bar_width, label='old')
plt.bar(br2, [combined[i][2] for i in range(len(combined))], color='r', width= bar_width, label='new')

# Label
plt.xlabel('Letters')
plt.ylabel('Frequency')
plt.xticks([r + bar_width for r in range(len(combined))], [combined[i][0] for i in range(len(combined))])

# Present window
plt.legend()
plt.show()