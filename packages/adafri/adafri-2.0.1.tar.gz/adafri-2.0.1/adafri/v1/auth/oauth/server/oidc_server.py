from authlib.integrations.flask_oauth2 import (
    AuthorizationServer,
    ResourceProtector,
)
from authlib.oauth2.rfc7636 import CodeChallenge
from ...oauth import (OAuthClient, OAuthToken, OpenIDAuthorizationCodeGrant as AuthCodeGrant, JwtTokenGenerator, JwtTokenValidator)
from ...oauth import OpenIDHybridGrant, OpenIDCode, RefreshTokenGrant
from authlib.integrations.flask_client import OAuth
import os
import requests

flask_oauth = OAuth();
provider = None;

# AuthorizationServer().a
class Server(AuthorizationServer):
    OAUTH2_REFRESH_TOKEN_GENERATOR = True
    
oidc_authorization_server = Server()
require_oidc_oauth = ResourceProtector()


def generate_token(client, grant_type, user=None, scope=None):
    print('generating token', client, grant_type, user, scope)
    return None;
def get_adafri_provider_cfg(base=None):
    if base is not None:
        discovery_url = base + "/.well-known/openid-configuration"
        return requests.get(discovery_url).json()
    return None

def config_oidc_oauth(app, query_client=None, save_token=None, token_generators=[]):
    flask_oauth.init_app(app)
    if query_client is None:
        query_client = OAuthClient().get_by_client_id
    if save_token is None:
        save_token = OAuthToken().save
    oidc_authorization_server.query_client = query_client
    oidc_authorization_server.save_token = save_token
    oidc_authorization_server.init_app(app)
    oidc_authorization_server.register_grant(AuthCodeGrant, [
        OpenIDCode(require_nonce=False),
        CodeChallenge(required=True)
    ])
    # oidc_authorization_server.register_grant(OpenIDImplicitGrant)
    oidc_authorization_server.register_grant(OpenIDHybridGrant)
    oidc_authorization_server.register_grant(RefreshTokenGrant)
    # for token_generator in token_generators:
    #     type = getattr(token_generator, 'type', None);
    #     generator = getattr(token_generator, 'generator', None);
    #     if None not in [type, generator]:
    #         oidc_authorization_server.register_token_generator(type, generator)
    # oidc_authorization_server.register_token_generator("default", TokenGenerator.generate)
    # oidc_authorization_server.register_token_generator("client_credentials", TokenGenerator.generate)
    oidc_authorization_server.register_token_generator("default", JwtTokenGenerator(issuer=os.getenv('JWT_ISSUER'), refresh_token_generator=generate_token))
    oidc_authorization_server.register_token_generator("client_credentials", JwtTokenGenerator(issuer=os.getenv('JWT_ISSUER'), refresh_token_generator=generate_token))
    require_oidc_oauth.register_token_validator(JwtTokenValidator(issuer=os.getenv('JWT_ISSUER'),
        resource_server=os.getenv('JWT_ISSUER')))
        
def guards_oidc(scopes=['profile'], request=None):
    """
    A decorator that checks if the user has the required scopes to access this route.

    Args:
        scopes (list): A list of scopes that the user must have to access this route.
        Defaults to ['profile'].

    Returns:
        The user's token if the user has the required scopes, otherwise None.
    """
    with require_oidc_oauth.acquire(scopes=scopes) as token:
        return token