import os
import requests
import database.crud as crud
from sqlalchemy.orm import Session

url = os.environ.get('CENSUS_URL')
api_key = os.environ.get('CENSUS_KEY')
headers = {'api-key': api_key}
params = {'in': 'state:',
            'for': 'tract:',
            'get': ''}

class GeographicTypes:
    async def convert_coordinates(latitude: str, longitude: str):
        geo_params = {
            'y' : longitude,
            'x': latitude, 
            'benchmark': '2020',
            'vintage': '2020',
            'format': 'json'
        }
        geo_url = os.environ.get('GEOCODE_URL')
        print(geo_url) 
        response = requests.get(geo_url, params=geo_params)
        result = response.json()

        if(result['result']['geographies'] == {}):
            return "Invalid Coordinates"

        data = {'state': result['result']['geographies']['Census Tracts'][0]['STATE'],
                'county': result['result']['geographies']['Census Tracts'][0]['COUNTY'],
                'tract': result['result']['geographies']['Census Tracts'][0]['TRACT'] }
        
        return data 
 
class CensusTypes:    
    async def get_census_data(db: Session, state: str, county: str, tract: str, section: str):
        
        data_points = crud.census_types.get_data_points(db, section)
        variables = data_points['variables']

        params['in'] += state + '%20county' + county
        params['for'] += tract
        params['get'] += variables

        response = requests.get(url, headers=headers, params=params)
        
        result = response.json()

        data = []

        i = 0
        for variable in result[1]:
            data.append({'label': data_points['labels'][i], 'variable': variable})

        return data 