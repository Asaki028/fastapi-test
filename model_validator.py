from pydantic import BaseModel, EmailStr, model_validator
from typing import List, Dict

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool 
    allergies: List[str]
    contact_details: Dict[str , str]

    @model_validator(mode='after')
    def validate_emergency_contact(cls,model):
        if model.age>60 and 'emergency_contact' not in model.contact_details:
            raise ValueError('Emergency contact is required for patients above 60 years old')
        return model
    

def update_patient_data(patient : Patient): 
    print(f"Updated patient data: {patient.name}, {patient.email}, {patient.age}, {patient.weight}, {patient.married}, {patient.allergies}, {patient.contact_details}")


patient_info = {'name': 'nishanta', 'email': 'nishant1@mit.com','age': 65, 'weight': 72.5, 'married': False, 'allergies': ['pollen', 'dust'], 'contact_details': {'email': 'abc123@gmail.com', 'phone': '674526326', 'emergency_contact': '9876543210'}}

patient1 = Patient(**patient_info)


update_patient_data(patient1)