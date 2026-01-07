

class ShortenerBaseError(Exception):
    pass

class NoLongUrlFoundError(ShortenerBaseError):
    pass

class DbError(ShortenerBaseError):
    ...