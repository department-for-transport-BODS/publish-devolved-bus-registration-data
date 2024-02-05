import os
from fastapi import FastAPI
from mangum import Mangum
from io import StringIO
from pydantic import BaseModel, Field, ValidationError, ValidationInfo, validator
from fastapi import FastAPI, File, UploadFile
import csv


# first_name,last_name,addresss
class person(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=5)
    last_name: str = Field(..., min_length=1, max_length=20)
    address: str


app = FastAPI()


@app.get("/")
def read_root():
    return {
        "message": "FastAPI running on AWS Lambda and is executed in region "
        + os.getenv("AWS_REGION", "Running locally")
        + ", using runtime environment "
        + os.getenv("AWS_EXECUTION_ENV", "Running locally")
    }


@app.get("/items")
def read_item():
    return {"item_id": 1}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    # Decode the CSV data
    csv_str = contents.decode("utf-8")
    # Convert the CSV data into a dictionary
    csv_data = list(csv.DictReader(StringIO(csv_str)))

    try:
        # Validate the data and deserialize it into a Python object.
        pydantic_model = [person(**data_dict) for data_dict in csv_data]
        print(pydantic_model)
        # with open("uploaded_file.csv", "wb") as f:
        #     f.write(contents)
        return {"filename": file.filename}
    except ValidationError as e:
        return e.errors()


lambda_handler = Mangum(app, lifespan="off")
