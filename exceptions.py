

class ShortenerBaseError(Exception):
    pass

class NoLongUrlFoundError(ShortenerBaseError):
    pass

class DbError(ShortenerBaseError):
    pass

class SlugGenerationError(ShortenerBaseError):
    pass
