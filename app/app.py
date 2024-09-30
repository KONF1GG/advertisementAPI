from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy import select

from lifespan import lifespan

from schema import GetAdvertisement, CreateAdvertisement, UpdateAdvertisement, StatusResponse, ItemId, \
    SearchAdvertisement
from dependencies import SessionDependencies
import crud
from models import Advertisement

app = FastAPI(
    title="advertisementAPI",
    version="1.0.0",
    lifespan=lifespan
)


@app.get('/v1/advertisement/{advertisement_id}', response_model=GetAdvertisement)
async def get_advertisements(advertisement_id: int, session: SessionDependencies):
    advertisement = await crud.get_item(session, Advertisement, advertisement_id)
    return advertisement.dict


@app.post('/v1/advertisement', response_model=ItemId)
async def create_advertisement(advertisement: CreateAdvertisement, session: SessionDependencies):
    advertisement = Advertisement(**advertisement.dict())
    advertisement = await crud.add_item(session, advertisement)
    return {'id': advertisement.id}


@app.patch('/v1/advertisement/{advertisement_id}', response_model=ItemId)
async def update_advertisement(advertisement_id: int, advertisement: UpdateAdvertisement, session: SessionDependencies):
    advertisement_orm = await crud.get_item(session, Advertisement, advertisement_id)
    for field, value in advertisement.dict(exclude_unset=True).items():
        setattr(advertisement_orm, field, value)
    advertisement_orm = await crud.add_item(session, advertisement_orm)
    return {'id': advertisement_orm.id}


@app.delete('/v1/advertisement/{advertisement_id}', response_model=StatusResponse)
async def delete_advertisement(advertisement_id: int, session: SessionDependencies):
    todo = await crud.get_item(session, Advertisement, advertisement_id)
    await session.delete(todo)
    await session.commit()
    return {'status': 'deleted'}


@app.get("/v1/advertisement", response_model=List[GetAdvertisement])
async def search_advertisements(session: SessionDependencies, advertisement: SearchAdvertisement = Depends()):
    query = select(Advertisement)


    if advertisement.title:
        query = query.where(Advertisement.title.ilike(f"%{advertisement.title}%"))
    if advertisement.description:
        query = query.where(Advertisement.description.ilike(f"%{advertisement.description}%"))
    if advertisement.min_price:
        query = query.where(Advertisement.price >= advertisement.min_price)
    if advertisement.max_price:
        query = query.where(Advertisement.price <= advertisement.max_price)
    if advertisement.author:
        query = query.where(Advertisement.author.ilike(f"%{advertisement.author}%"))

    result = await session.execute(query)
    advertisements = result.scalars().all()

    return advertisements
