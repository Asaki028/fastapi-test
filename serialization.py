from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pin: int

class Patient(BaseModel):
    
    name: str
    age: int
    gender: str = 'male'
    address: Address

address_dict = {'city': 'Guwahati', 'state': 'Assam', 'pin': 781001}
address1 = Address(**address_dict)

patient_dict = {'name': 'Nishanta', 'age': 22, 'gender': 'male', 'address': address1}

patient1 = Patient(**patient_dict)

#temp_dict = patient1.model_dump(exclude={'address': ['state']})  # or model_dump_json() if you want a JSON string instead of a dictionary. you've also got the option to include or exclude specific fields 

temp_dict = patient1.model_dump(exclude_unset=True)  # this will exclude any fields that were not explicitly set when creating the model instance. This can be useful for reducing the size of the serialized output and for avoiding sending unnecessary data over the network.
print(temp_dict)
print(type(temp_dict))