from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String

class Base(DeclarativeBase):
    pass

class ShortURL(Base):
    __tablename__ = "short_urls"
    slug: Mapped[str] = mapped_column(String(10),primary_key=True)
    long_url: Mapped[str] = mapped_column(String(256))