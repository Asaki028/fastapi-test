from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated;

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title='name', description='Patient\'s name', examples=['John'])]  # we can also use Annotated to add validation rules, in this case we are limiting the name to a maximum of 50 characters
    email: EmailStr   # custom data type in pydantic to validate email addresses

    Profile_url: Optional[AnyUrl] = None  # custom data type in pydantic to validate URLs, also we made it optional because not all patients may have a profile URL

    age: int = Field(gt=0, lt=100)
    weight: Annotated[float, Field(gt=0, strict=True)] ## we are using strict to ensure that the weight is always a float and not an integer, also we are validating that the weight is greater than 0
    married: Annotated[bool, Field(default=False, description='Indicates if the patient is married')] ## default value is false
    allergies: Annotated[Optional[List[str]], Field(default= None, max_length=5)] ## we didn't use just list because we also want to validate if the items inside the list are of type string or not

    contact_details: Dict[str , str]

def insert_patient_data(patient : Patient):
    print(f"Inserted patient data: {patient.name}, {patient.age}")

def update_patient_data(patient : Patient): 
    print(f"Updated patient data: {patient.name}, {patient.email}, {patient.Profile_url}, {patient.age}, {patient.weight}, {patient.married}, {patient.allergies}, {patient.contact_details}")


patient_info = {'name': 'Nishanta', 'email': 'nishant1@gmail.com','age': 22, 'weight': 72.5, 'married': False, 'allergies': ['pollen', 'dust'], 'contact_details': {'email': 'abc123@gmail.com', 'phone': '674526326'}}

patient1 = Patient(**patient_info)


update_patient_data(patient1)