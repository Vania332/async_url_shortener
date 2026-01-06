

class ShortenerBaseError():
    pass

class NoLongUrlFoundError(ShortenerBaseError):
    pass

class DbError(ShortenerBaseError):
    ...