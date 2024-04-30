import re
from fuzzywuzzy import fuzz
import fuzzy
import pgeocode
from data.processing_data import states

pingeocode = pgeocode.Nominatim('IN')

class TextAddress:
    soundex_weight = 0.2

    def __init__(self, address):
        self.original_address = str(address)
        self.address = address
        self.is_processed = False
        self.house_number = None
        self.pincode = None
        self.state = None
        self.state_list = None
        self.multiple_statenames = False
        self.city = None
        self.soundex_code = None

    def __lt__(self, other):
        return self.original_address < other.original_address

    def remove_quotes_commas(self):
        self.address = re.sub(r'[\'",]', ' ', self.address)
        return self.address


    def remove_punctuation(self):
        self.address = re.sub(r'[^\w\s\'"]', '', self.address)
        return self.address


    def remove_extra_whitespaces(self):
        self.address = ' '.join(self.address.split())
        return self.address
    

    def get_ascii_only(self):
        return re.sub(r'[^\x00-\x7F]', '', self.address)


    def extract_house_number(self):        
        matches = re.findall(r'\s*\S*\d+\S*\s', self.address)
        self.house_number = matches[0].strip() if matches else None
        return self.house_number


    def extract_pincode(self):
        pincode_pattern = re.compile(r'\b(\d{6})\b')
        match = re.search(pincode_pattern, self.address)
        self.pincode = match.group(1) if match else None
        return self.pincode
    
    def extract_pincode_info(self):
        self.extract_pincode()
        if self.pincode:
            pincode_info = pingeocode.query_postal_code(self.pincode)
            self.state = pincode_info.state_name
            self.city = pincode_info.county_name
            return {
                'pincode': self.pincode,
                'city': self.city,
                'state': self.state
            }
        else:
            return None

    def extract_state_name(self):
        state_pattern = r'\b(?:' + '|'.join(states.values()) + r')\b'    
        state_match = re.findall(state_pattern, self.address, flags=re.IGNORECASE)
        if len(state_match) == 1:
            self.state = state_match[0].title()
        elif len(state_match) > 1:
            self.state_list = state_match
            self.multiple_statenames = True
            self.state = state_match[-1].title()
            
        return self.state
        

    def exclude_common_terms(self): 
        common_address_terms = [
            "street", "road", "lane", "nagar", "marg", "cross", "avenue", "path", "bylane", "extension", "colony", "society", "plaza", 
            "market", "circle", "enclave", "terrace", "lane",
            "sector", "block", "phase", "area", "zone", "division",
            "north", "south", "east", "west", "n", "s", "e", "w",
            "near", "opposite", "next to", "behind", "adjacent to", "close to", "by", "facing", "across from",
            "tower", "building", "complex", "plaza", "mall", "apartment", "condo", "residence", "house", "villa",
            "flat", "apartment", "suite", "unit", "floor", "basement", "penthouse",
            "house", "home", "office", "shop", "store", "business", "school", "hospital", "temple", "church", "mosque",
            "sri", "sree", "shree", "jyoti", "sai", "green", "blue", "white", "royal", "golden",
            "main", "inner", "outer", "central", "new", "old", "upper", "lower", "middle",
            "gate", "view", "park", "garden", "lake", "river", "sky", "sun", "moon",
            "st", "rd", "ln", "ext", "col", "apt", "bldg", "fl", "opp",
            "township", "society", "nagar", "heights", "palace", "heritage", "residency"
        ]
        address = str(self.address)
        for term in common_address_terms:
            pattern = r'\b' + re.escape(term) + r'\b'
            address = re.sub(pattern, '', address)
        return ' '.join(address.split())


    def stardardize_states(self):
        words = self.address.split()
        for i in range(len(words)):
            if states.get(words[i]):
                words[i] = states[words[i]].lower()
        
        self.address = ' '.join(words)
        return self.address


    def preprocess_address(self):
        self.address = str(self.original_address)
        self.remove_quotes_commas()
        self.remove_extra_whitespaces()
        self.extract_house_number()
        self.remove_punctuation()
        self.address = self.address.lower()
        self.stardardize_states()
        self.extract_state_name()
        self.extract_pincode()
        self.is_processed = True
        return self.address


    def process_sound(self):
        if not self.is_processed:
            self.preprocess_address()
        
        soundex = fuzzy.Soundex(4)
        ascii_only_words = self.get_ascii_only().split()
        self.soundex_code = " ".join([soundex(word) for word in ascii_only_words])
        return self.soundex_code


    def compare_sound(self, other_address):
        self.process_sound()
        other_address.process_sound()
        return fuzz.token_sort_ratio(self.soundex_code, other_address.soundex_code)


    def compare_text(self, other_address):
        if not self.is_processed:
            self.preprocess_address()

        if not other_address.is_processed:
            other_address.preprocess_address()
    
        return (fuzz.token_sort_ratio(self.exclude_common_terms(), other_address.exclude_common_terms())*0.4
                + fuzz.WRatio(self.address, other_address.address))*0.6
    

    def compare_fuzz(self, other_address):
        if not self.is_processed:
            self.preprocess_address()

        if not other_address.is_processed:
            other_address.preprocess_address()

        return {
            'textMatchScore': self.compare_text(other_address),
            'soundMatchScore': self.compare_sound(other_address)
        }

    def fuzzy_match_score(self, other_address):
        text_score = self.compare_text(other_address)
        sound_score = self.compare_sound(other_address)
        return round(self.soundex_weight*sound_score + (1 - self.soundex_weight)*text_score, 2)
    

    def get_parsed_data(self):
        if not self.is_processed:
            self.preprocess_address()
        parsedData = {
            'houseNumber': self.house_number,
            'pincode': self.pincode,
            'state': self.state,
            'city': self.city
        }
        return { key: val for key, val in parsedData.items() if val is not None }  
    

