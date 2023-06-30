def dateProcessing(value):
    # DataCite expects ISO 8601 format OR YYYY-MM-DD OR YYYY OR date interval
    # https://inveniordm.docs.cern.ch/reference/metadata/#publication-date-1
    # TODO: Implement data processing
    return value

def authorProcessing(value):
    if value == "Person":
        return "personal"
    elif value == "Organization":
        return "organizational"
    else:
        return ""

def ISO8601Processing(value):
    return "ABC"