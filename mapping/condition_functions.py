def geonames(value):
    return True

def doi(value):
    """
        Checks if the value is a doi url
    """
    return value.startswith("https://doi.org/")