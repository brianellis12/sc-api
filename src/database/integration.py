import os
import requests
import database.crud as crud
from sqlalchemy.orm import Session

class GeographicTypes:

    # Query the Census Bureau GeoCode API to convert inputted coordinates to required Geographic Types
    async def convert_coordinates(latitude: str, longitude: str):
        
        # GeoCode URL Content 
        geo_params = {
            'y' : longitude,
            'x': latitude, 
            'benchmark': '2020',
            'vintage': '2020',
            'format': 'json'
        }
        geo_url = os.environ.get('GEOCODE_URL')
   
        response = requests.get(geo_url, params=geo_params)
        result = response.json()

        # Check if inputted Coordinates are valid and inside of the Untied States
        if(result['result']['geographies'] == {}):
            return "Invalid Coordinates"

        data = {'state': result['result']['geographies']['Census Tracts'][0]['STATE'],
                'county': result['result']['geographies']['Census Tracts'][0]['COUNTY'],
                'tract': result['result']['geographies']['Census Tracts'][0]['TRACT'] }
        
        return data
 
class CensusTypes:  

    # Retrieve the Necessary Variables and Labels from the database
    # Query the Census Bureau API for the Statistics of the retrieved variables 
    async def get_census_data(db: Session, state: str, county: str, tract: str, section: str):
        
        data_points = crud.CensusTypes.get_data_points(db, section)
        variables = data_points['variables']
        labels = data_points['labels']

        variables_string = ''.join([str(variable) + ',' for variable in variables])[:-1]

        # more processing to be done cleaning up labels def clean_label()
     
        # Census Variables URL Content
        url = os.environ.get('CENSUS_URL')
        api_key = os.environ.get('CENSUS_KEY')
        headers = {'api-key': api_key}
        params = {'in': 'state:' + state + '%20county:' + county,
                    'for': 'tract:' + tract,
                    'get': variables_string}

        # Get response
        response = requests.get(url, headers=headers, params=params)        
        result = response.json()

        # Format statistics from response with labels
        data = [{'label': labels[i], 'statistic': statistic} for i, statistic in enumerate(result[1][:-3])]

        return data