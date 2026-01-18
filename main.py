import string
from secrets import choice
from fastapi import Depends, FastAPI, Body, status, HTTPException
from fastapi.responses import RedirectResponse
from database.db import lifespan, AsyncSessionLocal
from database.repository import get_repo
from exceptions import NoLongUrlFoundError
from url_services import URLServices, get_services


app = FastAPI(lifespan=lifespan)


@app.post("/short-url")
async def generate_short_url(
    long_url: str = Body(embed=True),
    services: URLServices = Depends(get_services),
):
    short_url_obj = await services.create_short_url(long_url)
    
    return {
        "slug": short_url_obj.slug,
        "full": short_url_obj
            }


@app.get("/{slug}")
async def redirect_to_url(
    slug: str,
    services: URLServices = Depends(get_services),
    ):
    try:
        long_url = await services.get_long_url(slug)
    except NoLongUrlFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ссылка не существует"
        )
    return RedirectResponse(url=long_url, status_code=status.HTTP_302_FOUND)