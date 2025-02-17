from pyvenn import venn
from pyvenn.venn import venn5
import matplotlib.pyplot as plt
from itertools import chain, islice
from string import ascii_uppercase
from numpy.random import choice

# Define the sets
musicians = {
    "Members of The Beatles": {"Paul McCartney", "John Lennon", "George Harrison", "Ringo Starr"},
    "Guitarists": {"John Lennon", "George Harrison", "Jimi Hendrix", "Eric Clapton", "Carlos Santana"},
    "Played at Woodstock": {"Jimi Hendrix", "Carlos Santana", "Keith Moon"},
    "Solo Artists": {"Paul McCartney", "Eric Clapton", "Carlos Santana"},
    "Rock and Roll Hall of Fame": {"John Lennon", "George Harrison", "Ringo Starr", "Jimi Hendrix", "Eric Clapton"}
}

# Convert the sets to labels for venn5
labels = venn.get_labels([musicians[key] for key in musicians], fill=['number', 'logic'])

# Create the Venn diagram
fig, ax = venn5(labels, names=list(musicians.keys()))
plt.title("Musicians Venn Diagram")
plt.show()

# Additional example with random data

cmaps = ["cool", list("rgb"), "plasma", "viridis", "Set1"]
letters = iter(ascii_uppercase)

labels = venn.get_labels([dataset_dict[key] for key in dataset_dict], fill=['number', 'logic'])

venn.venn6(labels, names=list(dataset_dict.keys()), ax=ax)

plt.show()
