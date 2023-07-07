def is_uri(value):
    return value.startswith("http")

def is_not_uri(value):
    return not is_uri(value)

def geonames(value):
    return True

def doi(value):
    """
        Checks if the value is a doi url
    """
    return value.startswith("https://doi.org/")