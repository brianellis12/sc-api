import logging
import os
import requests
import database.crud as crud
from sqlalchemy.orm import Session

"""
Functions to get Geographic Data from external APIs
"""
class GeographicTypes:
    """
    Query the Census Bureau GeoCode API to convert inputted coordinates to required Geographic Types
    """
    async def convert_coordinates(latitude: str, longitude: str):
        logging.info(f"Entering convert_coordinates")
        logging.info(f"Converting coordinates {latitude}, {longitude} to GEOID")
        
        # GeoCode URL Content 
        geo_params = {
            'y' : longitude,
            'x': latitude, 
            'benchmark': '2020',
            'vintage': '2020',
            'format': 'json'
        }
        geo_url = os.environ.get('GEOCODE_URL')
   
        logging.info(f"Sending request to {geo_url} with params {geo_params}")
        response = requests.get(geo_url, params=geo_params)
        logging.info(f"Got response {response}")
        result = response.json()
        logging.info(f"Got result {result}")

        # Check if inputted Coordinates are valid and inside of the Untied States
        if(result['result']['geographies'] == {}):
            logging.error(f"Invalid coordinates")
            return "Invalid Coordinates"

        data = {'state': result['result']['geographies']['Census Tracts'][0]['STATE'],
                'county': result['result']['geographies']['Census Tracts'][0]['COUNTY'],
                'tract': result['result']['geographies']['Census Tracts'][0]['TRACT'] }
        
        logging.info(f"Got data {data}")
        logging.info(f"Exiting convert_coordinates")
        
        return data

"""
Functions to get Census Data from external APIs
"""
class CensusTypes:  
    """
    Retrieve the Necessary Variables and Labels from the database
    Query the Census Bureau API for the Statistics of the retrieved variables
    """ 
    async def get_census_data(db: Session, state: str, county: str, tract: str, section: str):
        logging.info(f"Entering get_census_data")
        logging.info(f"Getting census data for state {state}, county {county}, tract {tract}, section {section}")
        
        logging.info(f"Getting data points for section {section}")
        data_points = crud.CensusTypes.get_data_points(db, section)
        variables = data_points['variables']
        labels = data_points['labels']
        logging.info(f"Got {len(variables)} variables and {len(labels)} labels")

        variables_string = ''.join([str(variable) + ',' for variable in variables])[:-1]
     
        # Census Variables URL Content
        url = os.environ.get('CENSUS_URL')
        api_key = os.environ.get('CENSUS_KEY')
        headers = {'api-key': api_key}
        params = {'in': 'state:' + state + '%20county:' + county,
                    'for': 'tract:' + tract,
                    'get': variables_string}

        # Get response
        logging.info(f"Sending request to {url} with headers {headers} and params {params}")
        response = requests.get(url, headers=headers, params=params)        
        logging.info(f"Got response {response}")
        result = response.json()
        logging.info(f"Got result {result}")

        # Format statistics from response with labels
        data = [labels[i] + ': ' + statistic for i, statistic in enumerate(result[1][:-3])]
        logging.info(f"Got data {data}")
        
        logging.info(f"Exiting get_census_data")
        
        return data 