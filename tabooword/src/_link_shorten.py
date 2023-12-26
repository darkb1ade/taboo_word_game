import requests
import os


DOMAIN = "crt3.short.gy"
SHORT_URL = os.environ["SHORT_URL"]

def create_url(originalURL, pathname):
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": SHORT_URL,
    }
    url = "https://api.short.io/links"
    payload = {
        "originalURL": originalURL,
        "domain": DOMAIN,
        "path": pathname,
    }
    response = requests.post(url, json = payload, headers=headers)
    response = response.json()
    if "success" in response:
        return None
    else:
        return response["secureShortURL"] # success: False appear when fail

def get_url_id(pathname):
    headers = {
        "accept": "application/json",
        "Authorization": SHORT_URL
    }
    url = f"https://api.short.io/links/expand?domain={DOMAIN}&path={pathname}"
    response = requests.get(url, headers=headers)
    idString = response.json()['idString']
    return idString

def update_url(idString, originalURL):
    url = f"https://api.short.io/links/{idString}"
    payload = { "originalURL":  originalURL}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": SHORT_URL
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()["secureShortURL"]