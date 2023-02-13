from sqlalchemy.orm import Session
from app.geographic_types import model as geotype_model
from app.geographic_types import schema as geotype_schema
from app.census_data import model as census_model
from app.census_data import schema as census_schema

class geographic_types:
    @staticmethod
    def get(db: Session, longitude: any, latitude: any):
        geoid = ( 
            db.query(geotype_model.GeographicTypes)
            .filter(geotype_model.GeographicTypes.latitude == latitude)
            .filter(geotype_model.GeographicTypes.longitude == longitude)
            .first()            
        )
        return geoid

    @staticmethod
    def create(db: Session, geo_types: geotype_schema.GeographicTypesCreate):
        geo_type_model = geotype_model.GeographicTypes(**geo_types.dict())
        db.add(geo_type_model)
        db.commit()
        db.refresh(geo_type_model)
        return geo_type_model 

class census_types:
    @staticmethod
    def get_sections(db: Session, group: str):
        group_id = census_schema.CensusGroups.TRANSPORTATION
        sections = ( 
            db.query(census_model.CensusVariables.concept)
            .filter(census_model.CensusVariables.group == 'B23009')
            .distinct()
            .all()
        )
        print(sections)
        return sections
    
    @staticmethod
    def get_data_points(db: Session, section: str):

        result = ( 
            db.query(census_model.CensusVariables.label, census_model.CensusVariables.name)
            .filter(census_model.CensusVariables.concept == section)
            .all()
        )

        data_points = {
            'labels': [],
            'variables': []
        }
        for row in result:
            data_points['labels'].append(row[0])
            data_points['variables'].append(row[1])

        print(data_points)
        return data_points

    @staticmethod
    def create(db: Session, census_variables: census_schema.CensusVariablesCreate):
        census_variables_model = census_model.CensusVariables(**census_variables.dict())
        db.add(census_variables_model)
        db.commit()
        db.refresh(census_variables_model)
        return census_variables_model  
    