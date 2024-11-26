import httpx

from django.conf import settings

def exchange_code_for_token(code):
    # Keycloak token endpoint
    token_url = f"{settings.KEYCLOAK_HOST}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token?scope=openid"

    # Request parameters
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.KEYCLOAK_REDIRECT_URI,
        'client_id': settings.KEYCLOAK_CLIENT_ID,
        'client_secret': settings.KEYCLOAK_CLIENT_SECRET,
        'scope': 'openid',
    }

    # Make the POST request to retrieve the token
    response = httpx.post(token_url, data=data)
    response.raise_for_status()
    token = response.json()
    return token

def fetch_user_info(access_token):
    # Keycloak userinfo endpoint
    userinfo_url = f"{settings.KEYCLOAK_HOST}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/userinfo"

    # Add the access token to the Authorization header
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    # Make the GET request to fetch user information
    response = httpx.get(userinfo_url, headers=headers)
    response.raise_for_status()
    userinfo = response.json()
    return userinfo

# Example Usage
# token = exchange_code_for_token(code)
# userinfo = fetch_user_info(token['access_token'])