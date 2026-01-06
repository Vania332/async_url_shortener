import string
from secrets import choice
from fastapi import Depends, FastAPI, Body, status, HTTPException
from fastapi.responses import RedirectResponse
from database.db import lifespan, AsyncSessionLocal
from database.repository import URLRepository, get_repo
from exceptions import NoLongUrlFoundError

app = FastAPI(lifespan=lifespan)

ALPHABET = string.ascii_letters + string.digits 

def generate_random_slug() -> str:
    return ''.join(choice(ALPHABET) for _ in range(6))

@app.post("/short-url")
async def generate_short_url(
    long_url: str = Body(embed=True),
    repo: URLRepository = Depends(get_repo)
):
    short_url_obj = await repo.create_short_url(long_url)
    
    return {
        "slug": short_url_obj.slug,
        "full": short_url_obj
            }

@app.get("/{slug}")
async def redirect_to_url(
    slug: str,
    repo: URLRepository = Depends(get_repo)
    ):
    try:
        long_url = await repo.get_url_by_slug(slug)
    except NoLongUrlFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ссылка не существует"
        )
    return RedirectResponse(url=long_url.long_url, status_code=status.HTTP_302_FOUND)