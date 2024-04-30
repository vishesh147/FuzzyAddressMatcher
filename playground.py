from app.text_matcher import TextAddress
from fuzzywuzzy import fuzz
import fuzzy

addr1 = TextAddress("Narmada Bhuvan")
addr2 = TextAddress("Naramada Bhavan")

print(addr1.compare_fuzz(addr2))
