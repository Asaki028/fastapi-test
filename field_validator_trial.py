from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated;

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool 
    allergies: List[str]
    contact_details: Dict[str , str]

    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        valid_domains = ['mit.com', 'rwth-aachen.de', 'tu-berlin.de']
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        
        return value
    
    @field_validator('name')
    @classmethod
    def name_transformer(cls, value):
        return value.title() ## this will transform the name to title case, for example if we input 'nishanta' it will transform it to 'Nishanta'
    
def update_patient_data(patient : Patient): 
    print(f"Updated patient data: {patient.name}, {patient.email}, {patient.age}, {patient.weight}, {patient.married}, {patient.allergies}, {patient.contact_details}")


patient_info = {'name': 'nishanta', 'email': 'nishant1@mit.com','age': 22, 'weight': 72.5, 'married': False, 'allergies': ['pollen', 'dust'], 'contact_details': {'email': 'abc123@gmail.com', 'phone': '674526326'}}

patient1 = Patient(**patient_info)


update_patient_data(patient1)