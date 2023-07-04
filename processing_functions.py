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

def authorProcessing(value):
    if value == "Person":
        return "personal"
    elif value == "Organization":
        return "organizational"
    else:
        return ""

def ISO8601Processing(value):
    return "ABC"