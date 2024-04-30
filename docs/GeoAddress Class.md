# GeoAddress Class Documentation

The `GeoAddress` class is designed to process geographical addresses using the Bing Maps API. It provides methods to retrieve location data, calculate distances between addresses, and determine overlap between bounding boxes of addresses.

## Class Attributes:

- `api_key`: Bing Maps API key for accessing location data.
- `country_region`: Country or region code for the address (default is 'IN' for India).
- `max_results`: Maximum number of results to return from the API (default is 1).
- `output_type`: Output format for API response (default is 'json').
- `distance_factor`: Factor to adjust the impact of distance on the match score.
- `non_overlap_factor`: Factor to adjust the impact of non-overlapping bounding boxes on the match score.

## Class Methods:

### Initialization:
- `__init__(self, address_line)`: Constructor method to initialize the GeoAddress object with the provided address line.

### API Interaction:
- `process_json_response(self)`: Processes the JSON response from the Bing Maps API.
- `get_api_response(self)`: Sends a request to the Bing Maps API to retrieve location data.
- `get_json_response(self)`: Returns the JSON response from the Bing Maps API.

### Data Retrieval:
- `get_coords(self)`: Returns the coordinates (latitude, longitude) of the address.
- `get_bounding_box(self)`: Returns the bounding box coordinates of the address.
- `get_geo_data(self)`: Returns the complete location data of the address.

### Geospatial Analysis:
- `is_overlapping(self, other_geo_addr)`: Determines if the bounding boxes of two addresses overlap.
- `get_overlap_percentage(self, other_geo_addr)`: Calculates the percentage overlap between the bounding boxes of two addresses.
- `get_distance_km(self, other_geo_addr)`: Calculates the distance in kilometers between two addresses.

### Comparison and Matching:
- `compare_geo(self, other_geo_addr)`: Compares two addresses based on their geographical data.
- `geo_match_score(self, other_geo_addr)`: Calculates the match score between two addresses based on overlap and distance.

## External Libraries Used:
- `requests`: Library for making HTTP requests.
- `geopy.distance`: Library for calculating geographical distances.
- `shapely.geometry.Polygon`: Library for working with geometric shapes.

## Dependencies:
- Bing Maps API: Requires a valid API key for accessing location data.

## Example Usage:
```python
from GeoAddress import GeoAddress

# Initialize GeoAddresses
address1 = GeoAddress("1600 Pennsylvania Ave NW, Washington, DC 20500, USA")
address2 = GeoAddress("10 Downing St, Westminster, London SW1A 2AA, UK")

# Compare addresses
comparison_report = address1.compare_geo(address2)

print("Geo Match Score:", comparison_report['geoMatchScore'])
print("Overlap Status:", comparison_report['bboxOverlap'])
print("Distance (km):", comparison_report['distance'])
