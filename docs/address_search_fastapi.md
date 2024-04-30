# FastAPI Documentation

This FastAPI application provides endpoints for comparing and searching addresses. It utilizes the `TextAddress` and `GeoAddress` classes to perform text-based and geospatial comparisons.

## Endpoints:

### 1. /compare/
- **Method**: GET
- **Parameters**: 
    - `address1`: First address to compare (string)
    - `address2`: Second address to compare (string)
- **Description**: Compares two addresses using both text-based and geospatial methods.
- **Response**: 
    - `fuzzyMatchScore`: Fuzzy match score between the two addresses.
    - `fuzzyComparison`: Detailed comparison report based on text matching.
    - `geoComparison`: Detailed comparison report based on geospatial matching.
    - `address1Info`: Information about the parsed data and geolocation of the first address.
    - `address2Info`: Information about the parsed data and geolocation of the second address.

### 2. /search/
- **Method**: GET
- **Parameters**: 
    - `address`: Address to search for (string)
    - `max_limit`: Maximum number of matches to return (integer, default: 3)
    - `min_limit`: Minimum number of matches required to return (integer, default: 0)
- **Description**: Searches for similar addresses in the database based on the provided input address.
- **Response**: 
    - `inputAddress`: Information about the parsed data and geolocation of the input address.
    - `numberOfMatches`: Total number of matches found.
    - `matches`: List of matched addresses, each containing:
        - `matchedAddress`: The matched address.
        - `fuzzyMatchScore`: Fuzzy match score between the input address and the matched address.
        - `fuzzyComparison`: Detailed comparison report based on text matching.
        - `geoComparison`: Detailed comparison report based on geospatial matching.
        - `type`: Type of match (e.g., Perfect Match, Strong Match, Weak Match).
        - `addressInfo`: Information about the parsed data and geolocation of the matched address.

## Utility Functions:

### `get_match_type(fuzzy_match_score, geo_match_score)`
Determines the type of match based on the fuzzy match score and geospatial match score.

### `get_addresses_from_db()`
Retrieves addresses from the database and returns a list of address objects.

## External Libraries Used:
- `fastapi`: Framework for building APIs with Python.
- `sqlalchemy`: SQL toolkit and Object-Relational Mapping (ORM) library.
- `functools.cache`: Decorator for caching function results.
- `heapq`: Heap queue algorithm for finding top N matches.

## Dependencies:
- `app.text_matcher.TextAddress`: Class for text-based address matching.
- `app.geo_matcher.GeoAddress`: Class for geospatial address matching.
- `addresses.db`: SQLite database containing address information.

## Usage Example:
```python
# Importing the FastAPI application
from fastapi import FastAPI

# Create an instance of FastAPI
app = FastAPI()

# Define endpoints and functionality
...

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
