import os
from fastapi import FastAPI
from mangum import Mangum
from io import StringIO
from pydantic import BaseModel, Field, ValidationError, ValidationInfo, validator
from fastapi import FastAPI, File, UploadFile
import csv
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from .utils.csv_validator import Registration, validate_csv
from dotenv import load_dotenv
from .utils.logger import log

load_dotenv()
log.info(f"Running in regions: {os.getenv('AWS_REGION', 'Running locally')}")
log.info(f"Running in environment: {os.getenv('DB_HOST', 'Running locally')}")
# first_name,last_name,addresss
class person(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=5)
    last_name: str = Field(..., min_length=1, max_length=20)
    address: str


app = FastAPI()

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    return validate_csv(csv_data)

    # try:
    #     # Validate the data and deserialize it into a Python object.
    #     pydantic_model = [Registration(**data_dict) for data_dict in csv_data]
    #     print(pydantic_model)
    #     # with open("uploaded_file.csv", "wb") as f:
    #     #     f.write(contents)
    #     return {"filename": file.filename}
    # except ValidationError as e:
    #     '''If the data is invalid, FastAPI will raise a ValidationError exception.'''
    #     x = e.errors()
    #     import pprint
    #     pprint.pprint(x, indent=4)
    #     print(e.error_count())
    #     raise HTTPException(status_code=406, detail=e.errors())
    #     # return http request with status code 406 and error message


lambda_handler = Mangum(app, lifespan="off")
