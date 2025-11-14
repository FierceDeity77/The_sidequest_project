import requests
from django.conf import settings


def get_access_token():
    """Fetch a fresh OAuth token from Twitch (required for IGDB)."""
    api_endpoint = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET,
        "grant_type": "client_credentials"
    }

    response = requests.post(api_endpoint, params=params)
    data = response.json()

    return data.get("access_token", "")


def search_igdb_games(query):
    """Search IGDB games using a user-provided query."""
    api_endpoint = "https://api.igdb.com/v4/games"

    # Always get a fresh token (IGDB requires valid OAuth)
    # cache this in redis in the future for better performance
    token = get_access_token()

    headers = {
                "Client-ID": settings.CLIENT_ID,
                "Authorization": f"Bearer {token}"
            }


    # IGDB queries are written in a text query language, not JSON
    body = f"""
    search "{query}";
    fields id, name, first_release_date, platforms.name, cover.url, genres.name;
    limit 5;
    """

    response = requests.post(api_endpoint, headers=headers, data=body)
    data = response.json()

    return data

# print(search_igdb_games())