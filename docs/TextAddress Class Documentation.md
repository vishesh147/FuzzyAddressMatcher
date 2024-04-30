# TextAddress Class Documentation

The `TextAddress` class is designed to process and extract information from textual addresses. It utilizes various methods to preprocess and analyze the input address, including extracting house numbers, pin codes, state names, and removing common address terms.

## Class Attributes:

- `soundex_weight`: A class attribute representing the weightage of soundex comparison in the overall fuzzy match score.

## Class Methods:

### Initialization:
- `__init__(self, address)`: Constructor method to initialize the TextAddress object with the provided address.

### Text Processing:
- `remove_quotes_commas(self)`: Removes quotes and commas from the address.
- `remove_punctuation(self)`: Removes punctuation marks from the address.
- `remove_extra_whitespaces(self)`: Removes extra whitespaces from the address.
- `get_ascii_only(self)`: Removes non-ASCII characters from the address.
- `extract_house_number(self)`: Extracts the house number from the address.
- `extract_pincode(self)`: Extracts the pin code from the address.
- `extract_pincode_info(self)`: Extracts pin code information such as city and state using pgeocode library.
- `extract_state_name(self)`: Extracts the state name from the address.
- `exclude_common_terms(self)`: Excludes common address terms from the address.
- `stardardize_states(self)`: Standardizes state names in the address to lowercase.
- `preprocess_address(self)`: Performs all preprocessing steps on the address.

### Soundex Processing:
- `process_sound(self)`: Generates Soundex codes for each word in the address.
- `compare_sound(self, other_address)`: Compares Soundex codes of two addresses.

### Fuzzy Matching:
- `compare_text(self, other_address)`: Compares addresses using fuzzy matching without considering common address terms.
- `compare_fuzz(self, other_address)`: Compares addresses using both text and soundex matching methods.

### Utility Methods:
- `fuzzy_match_score(self, other_address)`: Calculates the overall fuzzy match score for two addresses.
- `get_parsed_data(self)`: Returns parsed address data including house number, pincode, state, and city.

## External Libraries Used:
- `re`: Python built-in library for regular expressions.
- `fuzzywuzzy`: Library for fuzzy string matching.
- `fuzzy`: Library for generating Soundex codes.
- `pgeocode`: Library for geocoding and reverse geocoding using postal codes.

## Dependencies:
- `data.processing_data.states`: A dictionary containing state abbreviations and full names.

## Example Usage:
```python
from TextAddress import TextAddress

# Initialize addresses
address1 = TextAddress("123 Main Street, Mumbai")
address2 = TextAddress("456 Main St, Mumbai, MH")

# Compare addresses
score = address1.fuzzy_match_score(address2)
parsed_data = address1.get_parsed_data()

print("Fuzzy Match Score:", score)
print("Parsed Address Data:", parsed_data)
