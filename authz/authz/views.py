from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import login
from keycloak import KeycloakOpenID
from urllib.parse import urlencode
from django.http import HttpResponse
from .service import exchange_code_for_token, fetch_user_info


def check(request):
    if request.user.is_authenticated:
        return HttpResponse("Welcome to the protected page!")

    # User is not authenticated, redirect to Keycloak SSO
    keycloak_login_url = settings.KEYCLOAK_AUTH_URL
    params = {
        "client_id": settings.KEYCLOAK_CLIENT_ID,
        "response_type": "code",  # OIDC authorization code flow
        "redirect_uri": settings.KEYCLOAK_REDIRECT_URI,
    }
    # Build the Keycloak login URL with query parameters
    login_url = f"{keycloak_login_url}?{urlencode(params)}"
    return redirect(login_url)


def oidc_callback(request):
    code = request.GET.get('code')

    if not code:
        return HttpResponse("Error: No authorization code returned from Keycloak.", status=400)

    token = exchange_code_for_token(code)
    userinfo = fetch_user_info(token['access_token'])
    # Exchange the authorization code for an access token
    # keycloak_openid = KeycloakOpenID(
    #     server_url=settings.KEYCLOAK_HOST.replace("localhost", "keycloak"),
    #     client_id=settings.KEYCLOAK_CLIENT_ID,
    #     realm_name=settings.KEYCLOAK_REALM,
    #     client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
    # )

    # token = keycloak_openid.token(
    #     grant_type='authorization_code',
    #     code=code,
    #     redirect_uri=settings.KEYCLOAK_REDIRECT_URI,
    #     scope="openid",
    # )
    # # print("HELLO WORLD!!!!")
    # # print(token)

    # userinfo = keycloak_openid.userinfo(token['access_token'])

    # Authenticate user in Django
    from django.contrib.auth.models import User
    user, created = User.objects.get_or_create(username=userinfo['preferred_username'])
    if created:
        user.first_name = userinfo.get('given_name', '')
        user.last_name = userinfo.get('family_name', '')
        user.email = userinfo.get('email', '')
        user.save()

    login(request, user)
    return redirect('http://localhost:9080/api/1/')
