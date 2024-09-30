from models import Session
from typing import Annotated
from fastapi import Depends


async def get_session():
    async with Session() as session:
        return session


SessionDependencies = Annotated[Session, Depends(get_session)]
