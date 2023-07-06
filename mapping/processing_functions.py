def dateProcessing(value):
    # DataCite expects ISO 8601 format OR YYYY-MM-DD OR YYYY OR date interval
    # https://inveniordm.docs.cern.ch/reference/metadata/#publication-date-1
    # TODO: Implement data processing
    return value

def geonamesProcessing(value):
    # map the geonmames url to the geonames id
    # example: "http://sws.geonames.org/8152662/"
    if (not value.startswith("http://sws.geonames.org/")):
        # not a geonnames url
        return None
    
    replaced_url = value.replace("http://sws.geonames.org/", "")
    replaced_url = replaced_url.replace("/", "")
    return replaced_url

def doi_processing(value):
    # check if value is doi format
    # example: "https://doi.org/10.4225/59/59672c09f4a4b"

    if (not value.startswith("https://doi.org/")):
        return None
    
    replaced_url = value.replace("https://doi.org/", "")
    return replaced_url

def authorProcessing(value):
    if value == "Person":
        return "personal"
    elif value == "Organization":
        return "organizational"
    else:
        return ""

def ISO8601Processing(value):
    return "ABC"