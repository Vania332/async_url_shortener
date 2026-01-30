from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
import string
from secrets import choice
from database.models import ShortURL

from database.db import get_session
from fastapi import Depends

from exceptions import NoLongUrlFoundError, SlugAlreadyExists

ALPHABET = string.ascii_letters + string.digits


class URLRepository():
    def __init__(self, session: AsyncSession):
        self.session = session 
    
    async def add_obj_to_database(self, short_url_obj: ShortURL):
        self.session.add(short_url_obj)
        try:
            await self.session.commit()
        except IntegrityError:
            raise SlugAlreadyExists
        await self.session.refresh(short_url_obj)
    
        
    async def get_url_by_slug(self, slug: str) -> ShortURL:
        result = await self.session.execute(select(ShortURL).where(ShortURL.slug == slug))
        long_url = result.scalar_one_or_none()
        if not long_url:
            raise NoLongUrlFoundError()
        return long_url
         

async def get_repo(session: AsyncSession = Depends(get_session)) -> URLRepository:
    return URLRepository(session)
