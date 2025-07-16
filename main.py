import json
from typing import Annotated, Literal, Optional
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException,Path, Query
from pydantic import BaseModel, Field, computed_field

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description='Id of patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='name of patient')]
    city: Annotated[str, Field(..., description='city where patient belongs to')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='age of patient')]
    gender: Annotated[Literal['male', 'female', 'other'], Field(..., description='gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='weight of the patient in kgs')]

    @computed_field
    @property 
    def bmi(self) -> float:
        return round(self.weight/(self.height**2),2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        if (self.bmi < 18.5):
            return 'Underweight'
        elif (self.bmi < 25):
            return 'Normal'
        elif (self.bmi < 30):
            return 'Overweight'
        else:
            return 'Obese'

def load_data():
    with open("patients.json", "r") as file:
        return json.load(file)
    
def update_data(data):
    with open("patients.json", "w") as file:
        return json.dump(data, file)

@app.get("/")
def home_page():
    return {"message": "Welcome to the Patient Management System API. Use the endpoints to manage patient data."}


@app.get("/patients")
def get_all_patients():
    json_data = load_data()
    return {"data": json_data}

@app.get("/patient/{patient_id}")
def get_patient_details(patient_id: str = Path(..., description="The ID of the patient to retrieve details for", 
                                               example="P001")):
    json_data = load_data()
    patient_data = json_data.get(patient_id)
    if not patient_data:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"data": patient_data}

@app.get("/patients/sorted")
def get_patient_in_sorted_order(
    sortby: str = Query(default="height", required=False, description="Sort the patient details by [age, weight, height] field"),
    order: str = Query(default="asc", required=False, description="Order of sorting: 'asc' for ascending, 'desc' for descending")
    ):
    json_data = load_data()

    if sortby not in ["age", "weight", "height"]:
        raise HTTPException(status_code=400, detail="Invalid sort field")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid sort order")
    
    patient_model_list = []
    for key, value in json_data.items():
        # convert dict to pydantic object
        value['id'] = key
        patient_model = Patient(**value)
        patient_model_list.append(patient_model)
    
    # sort list of pydantic models
    sorted_data_list = sorted(patient_model_list, key=lambda x: getattr(x, sortby), reverse=True if order == "desc" else False)

    # add id to the sorted data
    sorted_data = {}
    for patient in sorted_data_list:
        sorted_data[patient.id] = patient.model_dump(exclude='id')


    return {"data": sorted_data}

@app.post("/patient/create")
def create_patient(patient:Patient): # if there will be some invalid i/p it will throw error
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail='patient already exit')
    
    data[patient.id] = patient.model_dump(exclude=['id'])
    update_data(data)
    return JSONResponse(status_code=202, content='patient created suscessfully')

@app.delete('/patient/delete/{patient_id}')
def delete_patient(patient_id:str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='patient don\'t exists')
    # data.pop(patient_id)
    del data[patient_id]
    update_data(data)
    return JSONResponse(status_code=200, content='patient deleted suscessfully')


@app.patch('/patient/update')
def update_patient(patient: Patient):
    data = load_data()
    if patient.id not in data:
        raise HTTPException(status_code=404, detail='patient don\'t exists')
    data[patient.id] = patient.model_dump(exclude=['id'])
    update_data(data)
    return JSONResponse(status_code=200, content='patient updated suscessfully')


# giving flexibility to user to pass only modified values
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

@app.put('/patient/update/{patient_id}')
def update_patient_with_optional_fields(patient_id: str, patient_update: PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    #existing_patient_info -> pydantic object -> updated bmi + verdict
    existing_patient_info['id'] = patient_id
    patient_pydandic_obj = Patient(**existing_patient_info)
    #-> pydantic object -> dict
    existing_patient_info = patient_pydandic_obj.model_dump(exclude='id')
    # add this dict to data
    data[patient_id] = existing_patient_info
    # save data
    update_data(data)

    return JSONResponse(status_code=200, content={'message':'patient updated'})