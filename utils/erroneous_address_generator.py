import random
import re
import string


def shuffle_word_order(address):
    words = address.split()
    shuffled = words[1:-1]
    random.shuffle(shuffled)
    words[1:-1] = shuffled
    return ' '.join(words)

def remove_random_words(address, max_removals=2):
    words = address.split()
    
    if len(words) < max_removals + 3:
        max_removals = max(0, len(words) - 3)
    
    for _ in range(0, random.randint(0, max_removals)):
        words.pop(random.randint(0, len(words)-1))
    return ' '.join(words)

def generate_misspellings(address, number_of_words=2):
    alphabet = string.ascii_lowercase
    operations = [
        lambda s, index: s[:index] + random.choice(alphabet) + s[index:],
        lambda s, index: s[:index] + s[index + 1:] if len(s) > 1 else s,
        lambda s, index: s[:index] + random.choice(alphabet) + s[index + 1:]
    ]

    words = address.split()
    
    if len(words) < number_of_words:
        number_of_words = random.randint(1, len(words))

    random_words = random.sample(words, number_of_words)

    for i in range(len(words)):
        if words[i] in random_words:
            new_word = words[i]
            for _ in range(2): 
                operation = random.choice(operations)
                new_word = operation(new_word, random.randint(1, 3))
            words[i] = new_word
    
    return ' '.join(words)


# Define a list of possible transformations
transformations = [
    lambda address: re.sub(r'\b(?:road|rd)\b', 'Rd', address),                  # Replace 'road' with 'Rd'
    lambda address: re.sub(r'\b(?:street|st)\b', 'St', address),                # Replace 'street' with 'St'
    lambda address: re.sub(r'\b(?:avenue|ave)\b', 'Ave', address),              # Replace 'avenue' with 'Ave'
    lambda address: re.sub(r'\b(?:drive|dr)\b', 'Dr', address),                 # Replace 'drive' with 'Dr'
    lambda address: re.sub(r'\b(?:lane|ln)\b', 'Ln', address),                  # Replace 'lane' with 'Ln'
    lambda address: re.sub(r'\b(?:place|pl)\b', 'Pl', address),                 # Replace 'place' with 'Pl'
    lambda address: re.sub(r'\b(?:apartment|apt)\b', 'Apt', address),           # Replace 'apartment' with 'Apt'
    lambda address: re.sub(r'\b(?:building|bldg)\b', 'Bldg', address),          # Replace 'building' with 'Bldg'
    lambda address: re.sub(r'\b(?:suite|ste)\b', 'Ste', address),               # Replace 'suite' with 'Ste'
    lambda address: re.sub(r'\b(?:floor|flr)\b', 'Flr', address),               # Replace 'floor' with 'Flr'
    lambda address: re.sub(r'\b(?:block|blk)\b', 'Blk', address),               # Replace 'block' with 'Blk'
    lambda address: re.sub(r'\b(?:department|dept)\b', 'Dept', address),        # Replace 'department' with 'Dept'
    lambda address: re.sub(r'\b(?:number|no)\b', 'No', address),                # Replace 'number' with 'No'
]

def generate_erroneous_address(address):
    transformed_address = re.sub(r'[\'",]', ' ', address)
    transformed_address = generate_misspellings(transformed_address, number_of_words=random.randint(2, 4))
    transformed_address = shuffle_word_order(transformed_address)
    transformed_address = remove_random_words(transformed_address)

    for transformation in transformations:
        transformed_address = transformation(transformed_address)
    
    return transformed_address


addresses = open('data/addresses.txt', 'r')
erroneous_addresses = open('data/erroneous_addresses.txt','w')

for line in addresses:
    erroneous_addresses.write(f'{generate_erroneous_address(line.strip())}\n')
        
