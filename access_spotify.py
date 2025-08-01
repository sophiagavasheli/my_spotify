import json
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import requests

#access the spotify web API to get desired data

#get stuff from the .env file
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token} 

def get_artist(artist_id):
    """
    Get one artist based on spotify id
    """
    token = get_token() #access
    url = f"https://api.spotify.com/v1/artists/{artist_id}/"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result


def get_several_artists(artist_ids):
    """
    Takes a list of up to 50 artist Spotify IDs.
    Returns a list of artist JSON objects.
    """
    token = get_token()
    if not token:
        return []

    headers = get_auth_header(token)

    # Make sure we don't exceed 50 per request
    if len(artist_ids) > 50:
        raise ValueError("Maximum of 50 artist IDs allowed per request")

    ids_param = ",".join(artist_ids)
    url = f"https://api.spotify.com/v1/artists?ids={ids_param}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"[API ERROR] Failed batch request. Status: {response.status_code}")
        print(response.text)
        return []

    try:
        result = response.json()
        return result.get("artists", [])
    except json.JSONDecodeError:
        print(f"[JSON ERROR] Could not decode batch artist response")
        return []
