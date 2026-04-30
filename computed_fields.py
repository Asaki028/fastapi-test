from pydantic import BaseModel, EmailStr, computed_field
from typing import List, Dict

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    height: float
    married: bool 
    allergies: List[str]
    contact_details: Dict[str , str]

    @computed_field
    @property
    def bmi_calculate(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi
    
def update_patient_data(patient : Patient): 
    print(f"Updated patient data: {patient.name}, {patient.email}, {patient.age}, {patient.weight}, {patient.height}, {patient.married}, {patient.allergies}, {patient.contact_details}")
    print("BMI:", patient.bmi_calculate)

patient_info = {'name': 'nishanta', 'email': 'nishant1@mit.com','age': 65, 'weight': 72.5, 'height': 1.75, 'married': False, 'allergies': ['pollen', 'dust'], 'contact_details': {'email': 'abc123@gmail.com', 'phone': '674526326', 'emergency_contact': '9876543210'}}

patient1 = Patient(**patient_info)


update_patient_data(patient1)