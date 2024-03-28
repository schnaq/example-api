from typing import Optional

from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from api.auth import get_api_key

app = FastAPI()
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Stock(BaseModel):
    item_id: str
    availableStock: int


class Item(BaseModel):
    item_id: str
    sku: str
    qty_ordered: int


class Address(BaseModel):
    prefix: Optional[str]
    firstname: str
    middlename: Optional[str]
    lastname: str
    suffix: Optional[str]
    street: str
    house_number: str
    city: str
    telephone: str
    country_code: str
    country_name: str
    company: Optional[str]
    email: str
    additional_address_lines: Optional[list[str]]
    postcode: str
    state: str


class Fulfillment(BaseModel):
    shipping_address: Address
    items: list[Item]


class FulfillmentResponse(BaseModel):
    fulfillment_id: int
    status: str


# ----------------------------------------------------------------------------------------------------------------------

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/healthcheck")
def read_root():
    return {"status": "ok"}


# ----------------------------------------------------------------------------------------------------------------------

@app.get("/stock", response_model=list[Stock], dependencies=[Depends(get_api_key)])
def read_stock():
    stocks: list[Stock] = [
        Stock(item_id="LAGERBOX", availableStock=10),
        Stock(item_id="DRAHTKISTE", availableStock=20)
    ]
    return JSONResponse(content=jsonable_encoder(stocks))


@app.post("/fulfillment", response_model=FulfillmentResponse, dependencies=[Depends(get_api_key)])
def create_fulfillment(fulfillment: Fulfillment):
    return JSONResponse(content=jsonable_encoder(fulfillment))


@app.get("/fulfillment/{fulfillment_id}", response_model=Fulfillment, dependencies=[Depends(get_api_key)])
def read_fulfillment(fulfillment_id: int):
    response = FulfillmentResponse(fulfillment_id=fulfillment_id, status="shipped")
    return JSONResponse(content=jsonable_encoder(response))
