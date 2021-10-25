#Python
from os import path, stat
from typing import Optional
from enum import Enum
from fastapi.datastructures import Default

#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body,Query,Path,Form,Header, Cookie,UploadFile,File

app = FastAPI()

#Models
class HairColor(Enum):
    white = "white"
    black = "black"
    red = "red"

class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    age: int = Field(
        ...,
        gt = 0,
        lt = 115
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    email: EmailStr 

class Person(PersonBase):
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example":{
                "first_name":"Eduardo",
                "last_name":"Morales",
                "age":23,
                "hair_color":"black",
                "is_married":False,
                "email":"morales-martines19@hotmail.com",
                "password":"SoyYoDeNuevo"

            }
        }

class PersonOut(PersonBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    age: int = Field(
        ...,
        gt = 0,
        lt = 115
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    email: EmailStr 

class Location(BaseModel):
    city: str
    state: str
    country: str

class LoginOut(BaseModel):
    username: str = Field(...)
    message: str = Field(default= "Created succesfully")

class LoginIn(LoginOut):
    password: str = Field(...)

@app.get(
    path ="/",
    status_code= status.HTTP_200_OK)
def home():
    return {"Hello": "World"}

#REQUEST AND RESPONSE BODY
@app.post(
    path ="/person/new",
    response_model= PersonOut,
    status_code=status.HTTP_201_CREATED)
def create_person(person: Person = Body(...)):
    return person

#validations: Query parameters
@app.get(
    path = "/person/detail",
    status_code=status.HTTP_200_OK,
    deprecated= True)
def show_person(
    name: Optional[str]= Query(
        None,
        min_length = 1, 
        max_length=50,
        title = "Person Name",
        description = "This is the person name. Its optional"),
    age: str = Query(
        ...,
        title = "Age",
        description = "This is the person age. Its required")
):
    return {name: age}

#validations path parameters
people = [1,2,3,4,5]
@app.get(
    path = "/person/deatil/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Person"]
    )
def show_person(
    person_id: int = Path(
        ...,
        gt = 0,
        title = "Person id",
        description = "This is the person id. Its required")
):
    if person_id not in people:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "This person doesnt exist"
        )
    return {person_id: "its exist"}

#validations: request body
@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK)
def update_person(
    person_id: int = Path(
        ...,
        title = "Person id",
        description = "This is the person id",
        gt = 0
    ),
    person: Person = Body(
        ...
    ),
    # location: Location = Body(
    #     ...
    # )
):
    # result = person.dict()
    # result = result.update(location.dict)
    return person

#Forms
@app.post(
    path= "/login",
    status_code= status.HTTP_200_OK,
    response_model= LoginOut
)
def login(
    username: str = Form(...),
    password: str = Form(...)
):
    return LoginOut(username = username)

#Cookies and headers parameteres
@app.post(
    path = "/contact",
    status_code= status.HTTP_200_OK
)
def contact(
    first_name: str= Form(...),
    last_name: str = Form(...),
    message: str = Form(
        ...,
        min_length = 20
    ),
    email: EmailStr = Form(...),
    user_info: Optional[str]= Header(default = None),
    ads: Optional[str] = Cookie(default = None)

):
    return user_info

#Files
@app.post(path = "/post-image")

def post_image(
    image: UploadFile = File(...)
):
    """
    # Posting image
    This path show information about a uploaled photo by a form
    ## Parameters
        image: this image its uploaded by the user
    ## Response
        File-name: Name of the image
        Content-type: the format of the image
        Size(kb): Size in kbytes
    """
    return {
        "File-name":image.filename,
        "content-type": image.content_type,
        "size(kb)":round(len(image.file.read())/1024,2)

    }



