import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.census_data import model as census_model
from app.census_data import schema as census_schema
from app.user import model as user_model
from app.user import schema as user_schema

"""
Crud functions for application users 
"""
class user:
    """
    Get the user with the inputted id
    """
    @staticmethod
    def get(db: Session, id: int):
        logging.info(f"Entering get")
        logging.info(f"Querying user by id {id}")
        try:
            db_user = db.query(user_model.User).filter(user_model.User.id == id).first()
            if db_user is None:
                logging.error(f"User not found")
                raise HTTPException(status_code=404, detail="User not found")
            logging.info(f"Got user {db_user}")
        except Exception as e:
            logging.error(f"Query failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        logging.info(f"Exiting get")
        return db_user

    """
    Get all users
    """
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        logging.info(f"Entering get_all")
        logging.info(f"Querying all users with skip {skip} and limit {limit}")
        try:
            result = db.query(user_model.User).offset(skip).limit(limit).all()
            logging.info(f"Got {len(result)} users")
        except Exception as e:
            logging.error(f"Query failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        logging.info(f"Exiting get_all")
        return result

    """
    Add inputted user to the database
    """
    @staticmethod
    def create(db: Session, user: user_schema.UserCreate):
        logging.info(f"Entering create")
        logging.info(f"Creating user with data {user.dict()}")
        try:
            db_user = user_model.User(**user.dict())
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            logging.info(f"Created user {db_user}")
        except Exception as e:
            logging.error(f"Creation failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        logging.info(f"Exiting create")
        return db_user

    """
    Updated user associated to inputted it with inputted user data
    """
    @staticmethod
    def update(db: Session, id: int, updated_user: user_schema.UserCreate):
        logging.info(f"Entering update")
        logging.info(f"Updating user with id {id} and data {updated_user.dict()}")
        try:
            db_user = user.get(db, id) 
            db_user.first_name = updated_user.first_name
            db_user.last_name = updated_user.last_name
            db_user.practice_area = updated_user.practice_area
            db.commit()
            db.refresh(db_user) 
            logging.info(f"Updated user {db_user}")
        except Exception as e:
            logging.error(f"Update failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        logging.info(f"Exiting update")
        return db_user

"""
Crud functions for Census data 
"""
class CensusTypes:

    """
    Get Some Rows of the Census Variables table to verify if the database is populated
    """
    @staticmethod
    def get_all(db: Session):
        logging.info(f"Entering get_all")
        logging.info(f"Querying all census variables")
        try:
            result = db.query(census_model.CensusVariables).offset(0).limit(20).all()
            logging.info(f"Got {len(result)} census variables")
        except Exception as e:
            logging.error(f"Query failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        logging.info(f"Exiting get_all")
        return result

    """
    Return the sections of the inputted group 
    """
    @staticmethod
    def get_sections(db: Session, group: str):
        logging.info(f"Entering get_sections")
        logging.info(f"Querying sections for group {group}")
        try:
            sections = (  
                db.query(census_model.CensusVariables.section)
                .filter(census_model.CensusVariables.group.like(group + '%'))
                .distinct() 
                .all()
            )
            
            result = [pair['section'] for pair in sections]
            logging.info(f"Got {len(result)} sections")
        except Exception as e:
            logging.error(f"Query failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        logging.info(f"Exiting get_sections")
        return result

    """
    Get the variable and labels for the inputted section 
    """
    @staticmethod
    def get_data_points(db: Session, section: str):
        logging.info(f"Entering get_data_points")
        logging.info(f"Querying data points for section {section}")
        try:
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
            
            logging.info(f"Got {len(result['labels'])} labels and {len(result['variables'])} variables")
        except Exception as e:
            logging.error(f"Query failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        logging.info(f"Exiting get_data_points")
        return result
    
    """
    Add census variables to the database    
    """
    @staticmethod
    def create(db: Session, census_variables: census_schema.CensusVariablesCreate):
        logging.info(f"Entering create")
        logging.info(f"Creating census variables with data {census_variables.dict()}")
        try:
            census_variables_model = census_model.CensusVariables(**census_variables.dict())
            db.add(census_variables_model)
            db.commit()
            db.refresh(census_variables_model)
            logging.info(f"Created census variables {census_variables_model}")
        except Exception as e:
            logging.error(f"Creation failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        logging.info(f"Exiting create")
        return census_variables_model