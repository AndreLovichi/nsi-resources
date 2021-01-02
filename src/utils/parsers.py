def parseInteger(rawValue):
    if (rawValue.isnumeric()):
        return int(rawValue)
    else:
        return None

def parseDollarSum(rawString):
    cleanedString = rawString.replace("$", "").replace(",", "")
    return parseInteger(cleanedString)