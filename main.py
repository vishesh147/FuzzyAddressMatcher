from cgitb import text
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from functools import cache
import heapq

from app.text_matcher import TextAddress
from app.geo_matcher import GeoAddress

app = FastAPI()

def get_match_type(fuzzy_match_score, geo_match_score):
    if fuzzy_match_score == 100 and (geo_match_score is None or geo_match_score == 100):
        return 'Perfect Match'
    elif fuzzy_match_score > 80 and (geo_match_score is None or geo_match_score > 95):
        return 'Strong Match'
    elif fuzzy_match_score > 70 and (geo_match_score is None or geo_match_score > 90):
        return 'Good Match'
    elif fuzzy_match_score > 65:
        if geo_match_score is None or geo_match_score < 80:
            return 'Indeterministic'
        else:
            return 'Weak Match'
    else:
        return 'No Match'

@cache
def get_addresses_from_db():
    engine = create_engine('sqlite:///addresses.db')
    Base = automap_base()
    Base.prepare(engine)
    Address = Base.classes.Address
    session = Session(engine)
    result = session.query(Address).all()
    session.close()
    return result


@app.get("/compare/")
def compare(address1:str, address2:str):
    text_address1, text_address2 = TextAddress(address1), TextAddress(address2)
    geo_address1, geo_address2 = GeoAddress(address1), GeoAddress(address2)
    repsonse = {}
    repsonse['fuzzyMatchScore'] = text_address1.fuzzy_match_score(text_address2)
    repsonse['fuzzyComparison'] = text_address1.compare_fuzz(text_address2)
    repsonse['geoComparison'] = geo_address1.compare_geo(geo_address2)

    repsonse['address1Info'] = {
        'parsedData': text_address1.get_parsed_data(),
        'geoLocationData': geo_address1.get_geo_data()
    }
    repsonse['address2Info'] = {
        'parsedData': text_address2.get_parsed_data(),
        'geoLocationData': geo_address2.get_geo_data()
    }
    return repsonse


@app.get('/search/')
def search(address:str, max_limit:int = 3, min_limit:int = 0):
    response = {}
    text_input_address = TextAddress(address)
    geo_input_address = GeoAddress(address)

    response['inputAddress'] = {
        'parsedData': text_input_address.get_parsed_data(),
        'geoLocationData': geo_input_address.get_geo_data()
    }

    address_list = get_addresses_from_db()
    top_n_heap = []
    for address_item in address_list:
        text_address = TextAddress(address_item.address.strip())
        score = text_input_address.fuzzy_match_score(text_address)
        if len(top_n_heap) < max_limit:
            heapq.heappush(top_n_heap, (score, text_address))
        else:
            if score > top_n_heap[0][0]:
                heapq.heappop(top_n_heap)
                heapq.heappush(top_n_heap, (score, text_address))
    
    top_n_heap = sorted(top_n_heap, reverse=True)
    max_score = top_n_heap[0][0]

    error_margin = 5

    response['numberOfMatches'] = 0
    response['matches'] = []

    for score, text_address in top_n_heap:
        if score > max_score - error_margin:
            geo_address = GeoAddress(text_address.original_address)
            match_data = {}
            match_data['matchedAddress'] = text_address.original_address
            match_data['fuzzyMatchScore'] = score
            match_data['fuzzyComparison'] = text_input_address.compare_fuzz(text_address)
            match_data['geoComparison'] = geo_input_address.compare_geo(geo_address)
            geo_match_score = match_data['geoComparison'].get('geoMatchScore', None)

            match_data['type'] = get_match_type(score, geo_match_score)
            match_data['addressInfo'] = {
                'parsedData': text_address.get_parsed_data(),
                'geoLocationData': geo_address.get_geo_data()
            }
            if match_data['type'] != 'No Match' or score > 75 or len(response['matches']) < min_limit:
                response['matches'].append(match_data)
        else:
            break

    response['numberOfMatches'] = len(response['matches'])

    return response
