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
        db_user = db.query(user_model.User).filter(user_model.User.id == id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user

    """
    Get all users
    """
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        print("here")
        return db.query(user_model.User).offset(skip).limit(limit).all()

    """
    Add inputted user to the database
    """
    @staticmethod
    def create(db: Session, user: user_schema.UserCreate):
        db_user = user_model.User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    """
    Updated user associated to inputted it with inputted user data
    """
    @staticmethod
    def update(db: Session, id: int, updated_user: user_schema.UserCreate):
        db_user = user.get(db, id) 
        db_user.first_name = updated_user.first_name
        db_user.last_name = updated_user.last_name
        db_user.practice_area = updated_user.practice_area
        db.commit()
        db.refresh(db_user) 
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
        return db.query(census_model.CensusVariables).offset(0).limit(20).all()

    """
    Return the sections of the inputted group 
    """
    @staticmethod
    def get_sections(db: Session, group: str):
        sections = (  
            db.query(census_model.CensusVariables.section)
            .filter(census_model.CensusVariables.group.like(group + '%'))
            .distinct() 
            .all()
        )
        
        result = [pair['section'] for pair in sections]
        return result

    """
    Get the variable and labels for the inputted section 
    """
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
    
    """
    Add census variables to the database    
    """
    @staticmethod
    def create(db: Session, census_variables: census_schema.CensusVariablesCreate):
        census_variables_model = census_model.CensusVariables(**census_variables.dict())
        db.add(census_variables_model)
        db.commit()
        db.refresh(census_variables_model)
        return census_variables_model  
    
