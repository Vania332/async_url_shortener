from pydantic import BaseModel, HttpUrl


class URLSchema(BaseModel):
    long_url: HttpUrl
    slug: str
    