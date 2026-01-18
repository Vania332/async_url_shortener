import string
from secrets import choice

from fastapi import Depends
from database.repository import get_repo
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import ShortURL
from database.repository import URLRepository
from exceptions import SlugGenerationError, NoLongUrlFoundError

ALPHABET = string.ascii_letters + string.digits


class URLServices():
    def __init__(self, repo: URLRepository):
        self.repo = repo
    
    
    async def create_short_url(self, long_url: str) -> ShortURL:
        slug = await self._generate_unique_slug()
        short_url_obj = ShortURL(slug=slug, long_url=long_url)
        await self.repo.add_obj_to_database(short_url_obj)
        return short_url_obj
    
    
    async def get_long_url(self, slug: str) -> str:
        short_url = await self.repo.get_url_by_slug(slug)
        return short_url.long_url
    
    
    async def _generate_unique_slug(self, lenth: int = 6, max_attempts: int = 10) -> str:
        for _ in range(max_attempts):
            slug = self._generate_slug()
            try:
                await self.repo.get_url_by_slug(slug)
            except NoLongUrlFoundError:
                return slug
        raise SlugGenerationError()
    
    
    def _generate_slug(self):
        return ''.join(choice(ALPHABET) for _ in range(6))
    
async def get_services(session: AsyncSession = Depends(get_repo)) -> URLServices:
    return URLServices(session)
