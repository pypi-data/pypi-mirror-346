import functools


class BactaxError(Exception):

    @classmethod
    def enforce_error_type(cls, func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception as error:
                if not isinstance(error, cls):
                    raise cls() from error
                else:
                    raise
            else:
                return result

        return wrapper


class TaxonomyFileNotFoundError(FileNotFoundError, BactaxError):

    def __init__(self):
        msg = "No taxonomy data file was found. Please download it using `bactax.update()`"
        super().__init__(msg)


class NoTaxonomyDataError(BactaxError):

    def __init__(self, **kwargs):
        constraints = [f"{k}={repr(v)}" for k, v in kwargs.items()]
        msg = f"Taxonomy information was not found for the provided input: {', '.join(constraints)}"
        super().__init__(msg)


class DmpParseError(BactaxError):

    def __init__(self):
        msg = "An error occured parsing the .dmp file"
        super().__init__(msg)
