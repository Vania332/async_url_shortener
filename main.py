import string
from secrets import choice
from fastapi import Depends, FastAPI, Body, status, HTTPException
from fastapi.responses import RedirectResponse
from database.db import lifespan, AsyncSessionLocal
from database.repository import get_repo
from exceptions import NoLongUrlFoundError, SlugAlreadyExists, NotURLInserted
from url_services import URLServices, get_services
from schemas import URLSchema
#---------------------------------------------------------------------------------------------------
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


app = FastAPI(lifespan=lifespan)


@app.post("/short-url")
async def generate_short_url(
    data: URLSchema,
    services: URLServices = Depends(get_services),
):
    
    long_url = str(data.long_url)
    try:
        short_url_obj = await services.create_short_url(long_url)
    except SlugAlreadyExists:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Не удалось создать slug")
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