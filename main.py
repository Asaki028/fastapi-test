from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()


class Patient(BaseModel):

    id: Annotated[str, Field(..., description="The ID of the patient", example="P001")]
    name: Annotated[str, Field(..., description="The name of the patient")]
    city: Annotated[str, Field(..., description="The city where the patient lives")]
    age: Annotated[int, Field(..., gt=0, lt=100, description="The age of the patient")] 
    gender: Annotated[Literal['male', 'female','other'], Field(..., description="The gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="The height of the patient in meters")]
    weight: Annotated[float, Field(..., gt=0, description="The weight of the patient in kilograms")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi
    
    @computed_field
    @property
    def verdicts(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif 18.5 <= self.bmi < 25:
            return 'Normal weight'
        elif 25 <= self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obesity'
        

class UpdatePatient(BaseModel):

    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=100)]
    gender: Annotated[Optional[Literal['male', 'female','other']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

    
def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
        return data
    
def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get('/about')
def about():
    return {"message": "A fully functional patient management system API built with FastAPI."}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def get_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", example="P001")):
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'), order: str = Query('asc', description='sort in asc or desc order')):
    valid_fields = ['height', 'weight', 'bmi']
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by value. Must be one of {valid_fields}")
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order value. Must be 'asc' or 'desc'")
    
    data = load_data()

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse= sort_order)

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient with this ID already exists')
    
    data[patient.id] = patient.model_dump(exclude={'id'})

    save_data(data)

    return JSONResponse(content={"message": "Patient created successfully"}, status_code=201)

@app.put('/update/{patient_id}')
def update_patient(patient_id: str, updated_patient: UpdatePatient):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_data = data[patient_id]
    updated_patient_data = updated_patient.model_dump(exclude_unset=True)

    for key,value in updated_patient_data.items():
        existing_patient_data[key] = value

    existing_patient_data['id'] = patient_id
    new_pydantic_patient = Patient(**existing_patient_data)
    existing_patient_data = new_pydantic_patient.model_dump(exclude={'id'})
    data[patient_id] = existing_patient_data
    save_data(data)
    return JSONResponse(content={"message": "Patient updated successfully"}, status_code=200)


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    del data[patient_id]
    save_data(data)

    return JSONResponse(content={"message": "Patient deleted successfully"}, status_code=200)