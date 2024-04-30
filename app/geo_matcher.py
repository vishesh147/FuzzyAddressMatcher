import requests
import geopy.distance
from shapely.geometry import Polygon

class GeoAddress:
    api_key = 'AqhKeXzvAgR_eos6SLlcVxcMrgk1jf__JZjKdSZPQnGmLUpmP6JPm8kILuxebwM2'
    country_region = 'IN'
    max_results = 1
    output_type = 'json'
    distance_factor = 2
    non_overlap_factor = 0.05

    def __init__(self, address_line):
        self.address_line = address_line
        self.location_data = {}
        self.json_response = None
        self.status_code = None


    def process_json_response(self):
        if not self.status_code:
            self.get_api_response()

        resourceSets = self.json_response['resourceSets']
        if len(resourceSets) > 0 and resourceSets[0]['estimatedTotal'] > 0:
            resource = resourceSets[0]['resources'][0]
            self.location_data['boundingBox'] = resource.get('bbox', None)
            point = resource.get('point', None)
            if point:
                self.location_data['coordinates'] = point.get('coordinates', None)
            self.location_data['confidence'] = resource.get('confidence', None)
            self.location_data['mapAddress'] = resource.get('address', None)
            if self.location_data['mapAddress']:
                if self.location_data['mapAddress'].get('adminDistrict', None):
                    self.location_data['mapAddress']['state'] =  self.location_data['mapAddress'].pop('adminDistrict')
                if self.location_data['mapAddress'].get('adminDistrict2', None):
                    self.location_data['mapAddress']['district'] =  self.location_data['mapAddress'].pop('adminDistrict2')
                if self.location_data['mapAddress'].get('locality', None):
                    self.location_data['mapAddress']['city'] =  self.location_data['mapAddress'].pop('locality')


    def get_api_response(self):
        url = f'''http://dev.virtualearth.net/REST/v1/Locations?
                countryRegion={self.country_region}
                &addressLine={self.address_line}
                &key={self.api_key}
                &maxResults={self.max_results}
                &o={self.output_type}'''
        
        response = requests.get(url)
        self.status_code = response.status_code
        if response.status_code == 200:
            self.json_response = response.json()
            if self.json_response:
                self.process_json_response()
        return response


    def get_json_response(self):
        if not self.status_code:
            self.get_api_response()
        return self.json_response
    

    def get_coords(self):
        if not self.status_code:
            self.get_api_response()

        return self.location_data.get('coordinates', None)
    

    def get_bounding_box(self):
        if not self.status_code:
            self.get_api_response()
        return self.location_data.get('boundingBox', None)
    

    def get_geo_data(self):
        if not self.status_code:
            self.get_api_response()
        return self.location_data


    def is_overlapping(self, other_geo_addr):
        if not self.status_code:
            self.get_api_response()

        if not other_geo_addr.status_code:
            other_geo_addr.get_api_response()

        is_overlapping = None

        if (not self.location_data) or (not other_geo_addr.location_data):
            return None
        
        bbox1 = self.location_data.get('boundingBox', None)
        bbox2 = other_geo_addr.location_data.get('boundingBox', None)

        if bbox1 and bbox2:
            if (bbox1[0] > bbox2[2] or bbox1[2] < bbox2[0] or
                bbox1[1] > bbox2[3] or bbox1[3] < bbox2[1]):
                is_overlapping = False
            else:
                is_overlapping = True

        return is_overlapping
    
    def get_overlap_percentage(self, other_geo_addr):
        if not self.status_code:
            self.get_api_response()

        if not other_geo_addr.status_code:
            other_geo_addr.get_api_response()
        
        bbox1 = self.location_data.get('boundingBox', None)
        bbox2 = other_geo_addr.location_data.get('boundingBox', None)

        if not bbox1 or not bbox2:
            return None

        poly1 = Polygon([(bbox1[1], bbox1[0]),
                        (bbox1[1], bbox1[2]),
                        (bbox1[3], bbox1[2]),
                        (bbox1[3], bbox1[0])])

        poly2 = Polygon([(bbox2[1], bbox2[0]),
                        (bbox2[1], bbox2[2]),
                        (bbox2[3], bbox2[2]),
                        (bbox2[3], bbox2[0])])
        
        intersection = poly1.intersection(poly2)

        if intersection.is_empty:
            return 0
        else:
            overlap_area = intersection.area
            average_area = (poly1.area + poly2.area) / 2
            overlap_percentage = (overlap_area / average_area) * 100
            return round(overlap_percentage, 2)


    def get_distance_km(self, other_geo_addr):   
        if not self.status_code:
            self.get_api_response()

        if not other_geo_addr.status_code:
            other_geo_addr.get_api_response()

        distance = None
        if other_geo_addr.get_coords() and self.get_coords():
            distance = geopy.distance.geodesic(other_geo_addr.get_coords(), self.get_coords()).km
        return distance


    def compare_geo(self, other_geo_addr):
        if not self.status_code:
            self.get_api_response()

        if not other_geo_addr.status_code:
            other_geo_addr.get_api_response()

        report = {}
        report['geoMatchScore'] = self.geo_match_score(other_geo_addr)
        report['bboxOverlap'] = self.is_overlapping(other_geo_addr)
        report['distance'] = self.get_distance_km(other_geo_addr)
        
        return { key: val for key, val in report.items() if val is not None }  
        

    def geo_match_score(self, other_geo_addr):
        if not self.status_code:
            self.get_api_response()

        if not other_geo_addr.status_code:
            other_geo_addr.get_api_response()

        distance_km = self.get_distance_km(other_geo_addr)
        overlap_percentage = self.get_overlap_percentage(other_geo_addr)
        
        if overlap_percentage:
            return round(100 - (100 - overlap_percentage)*self.non_overlap_factor, 2)
        if distance_km:
            return round(max(0, 90 - distance_km*self.distance_factor), 2)
        else:
            return None
