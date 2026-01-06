from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import string
from secrets import choice
from database.models import ShortURL

from database.db import get_session
from fastapi import Depends

from exceptions import NoLongUrlFoundError

ALPHABET = string.ascii_letters + string.digits


class URLRepository():
    def __init__(self, session: AsyncSession):
        self.session = session 
    
    def generate_slug(self):
        return ''.join(choice(ALPHABET) for _ in range(6))
    
    async def create_short_url(self, long_url: str) -> ShortURL:
        slug = self.generate_slug()
        while await self.get_url_by_slug(slug):
            slug = self.generate_slug()
        short_url_obj = ShortURL(slug=slug, long_url=long_url)
        self.session.add(short_url_obj)
        await self.session.commit()
        await self.session.refresh(short_url_obj)
        return short_url_obj
        
    async def get_url_by_slug(self, slug: str) -> ShortURL:
        result = await self.session.execute(select(ShortURL).where(ShortURL.slug == slug))
        long_url = result.scalar_one_or_none()
        if not long_url:
            raise NoLongUrlFoundError()
        return long_url
         

async def get_repo(session: AsyncSession = Depends(get_session)) -> URLRepository:
    return URLRepository(session)