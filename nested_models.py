from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pin: int

class Patient(BaseModel):
    
    name: str
    age: int
    gender: str
    address: Address

address_dict = {'city': 'Guwahati', 'state': 'Assam', 'pin': 781001}
address1 = Address(**address_dict)

patient_dict = {'name': 'Nishanta', 'age': 22, 'gender': 'male', 'address': address1}

patient1 = Patient(**patient_dict)

print(patient1)
print(patient1.address.city)
print(patient1.address.state)


## NOTES : We use nested models in pydantic to represent complex data structures,e.g, the "address" field which contains complex data that would be difficult to retrieve otherwise. In this example, we have an Address model that is nested inside the Patient model. This allows us to organize our data in a more structured way and also makes it easier to validate the data. We can create an instance of the Address model and then use it to create an instance of the Patient model.