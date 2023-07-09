def is_uri(value):
    return value and value.startswith("http")

def is_not_uri(value):
    return value and not is_uri(value)

def geonames(value):
    return True

def doi(value):
    """
        Checks if the value is a doi url
    """
    return value and value.startswith("https://doi.org/")

def orcid(value):
    return value and value.startswith("https://orcid.org/")

def embargoed(value):
    """
        Checks if the value is a date in the future.
    """
    import pytz
    from dateutil.parser import parse
    from datetime import datetime

    utc=pytz.UTC

    if value == None:
        return False

    fuzzy_date = parse(value, fuzzy=True)
    now = datetime.now()
    if (now.timestamp() < fuzzy_date.timestamp()):
        return True
    return False

def string(value):
    return value and isinstance(value, str)