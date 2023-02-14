from sqlalchemy.orm import Session
from app.census_data import model as census_model
from app.census_data import schema as census_schema

class CensusTypes:

    # Get Some Rows of the Census Variables table to verify if the database is populated
    @staticmethod
    def get_all(db: Session):
        return db.query(census_model.CensusVariables).offset(0).limit(20).all()

    # Return the sections of the inputted group 
    @staticmethod
    def get_sections(db: Session, group: str):
        group_id = census_schema.CensusGroups[group].value
        
        group_str = str(group_id) + '%'

        sections = (  
            db.query(census_model.CensusVariables.section)
            .filter(census_model.CensusVariables.group.like(group_str))
            .distinct() 
            .all()
        )
        
        return sections

    # Get the variable and labels for the inputted section
    @staticmethod
    def get_data_points(db: Session, section: str):
        query_result = ( 
            db.query(census_model.CensusVariables.label, census_model.CensusVariables.variable)
            .filter(census_model.CensusVariables.section == section) 
            .all()
        )

        # Format Result
        result = {'labels': [],
        'variables': []}

        for row in query_result:
            result['labels'].append(row['label'])
            result['variables'].append(row['variable'])

        return result

    # Add census variables to the database
    @staticmethod
    def create(db: Session, census_variables: census_schema.CensusVariablesCreate):
        census_variables_model = census_model.CensusVariables(**census_variables.dict())
        db.add(census_variables_model)
        db.commit()
        db.refresh(census_variables_model)
        return census_variables_model  
    