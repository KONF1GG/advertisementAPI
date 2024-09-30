from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from models import Session, Advertisement, ORM_CLS, ORM_OBJ


async def add_item(session: Session, item: Advertisement) -> ORM_OBJ:
    session.add(item)
    try:
        await session.commit()
    except IntegrityError as err:
        if err.orig.pgcode == '23505':
            raise HTTPException(status_code=409, detail='Item already exists')
        raise err
    return item


async def get_item(session: Session, orm_cls: ORM_CLS, item_id: int) -> ORM_OBJ:
    orm_obj = await session.get(orm_cls, item_id)
    if orm_obj is None:
        raise HTTPException(status_code=404, detail=f'{orm_cls.__name__} not found with id {item_id}')
    return orm_obj

# async def update_item(session: Session, orm_cls: ORM_CLS, item_id: int) -> ORM_OBJ:
