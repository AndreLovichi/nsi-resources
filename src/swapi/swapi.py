import json
import requests

BASE_URL = "https://swapi.dev/api/"

def fetchFromSwapi(url):
    results = []
    fetching = True
    nextUrl = url

    while(fetching):
        rawResponse = requests.get(nextUrl)
        response = json.loads(rawResponse.content.decode("utf-8"))

        results.extend(response["results"])
        
        if(response["next"] is None):
            fetching = False
        else:
            nextUrl = response["next"]

    return results