# Address Transformation Functions Documentation

The address transformation functions in this module are designed to generate variations of input addresses by shuffling word order, removing random words, introducing misspellings, and applying common transformations.

## Functions:

### shuffle_word_order(address)
Shuffles the order of words in the address, excluding the first and last words (e.g., street numbers and postal codes).

### remove_random_words(address, max_removals=2)
Removes a random number of words from the address, with an upper limit defined by the `max_removals` parameter.

### generate_misspellings(address, number_of_words=2)
Introduces misspellings in a random selection of words in the address. The number of misspelled words is determined by the `number_of_words` parameter.

### generate_erroneous_address(address)
Generates an erroneous version of the address by applying a combination of transformations. This includes shuffling word order, removing random words, introducing misspellings, and applying common address transformations.

## Common Transformations:
- Replace 'road' with 'Rd'
- Replace 'street' with 'St'
- Replace 'avenue' with 'Ave'
- Replace 'drive' with 'Dr'
- Replace 'lane' with 'Ln'
- Replace 'place' with 'Pl'
- Replace 'apartment' with 'Apt'
- Replace 'building' with 'Bldg'
- Replace 'suite' with 'Ste'
- Replace 'floor' with 'Flr'
- Replace 'block' with 'Blk'
- Replace 'department' with 'Dept'
- Replace 'number' with 'No'

## Usage Example:
```python
# Importing the functions
from address_transformations import shuffle_word_order, remove_random_words, generate_misspellings, generate_erroneous_address

# Generate an erroneous version of the address
original_address = "123 Main Street, Springfield"
erroneous_address = generate_erroneous_address(original_address)

print("Original Address:", original_address)
print("Erroneous Address:", erroneous_address)
