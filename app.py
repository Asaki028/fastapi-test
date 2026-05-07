from fastapi import FastAPI
from pydantic import BaseModel, computed_field, Field
from typing import Literal, Annotated
import pickle
import pandas as pd

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

app = FastAPI()

class InputData(BaseModel):
    age: Annotated[int, Field(...,gt=0, lt=100, description="Age must be between 1 and 99", example=30)]
    weight: Annotated[float, Field(..., gt =0, example=70.5)]
    height: Annotated[float, Field(..., gt =0, example=175.0)]
    income_lpa: Annotated[float, Field(..., gt=0, example=5.0)]
    smoker: Annotated[bool, Field(..., example='no')]
    city: Annotated[str, Field(..., example='New York')]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(..., example='Engineer')] 
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height** 2)
    
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"