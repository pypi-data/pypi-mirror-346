from protean_streamlit.utils import (
    get_bearer_token,
    validate_bearer_token,
    update_session_store,
    get_key_set,
)


class ProteanAuthenticator:
    """
    This class manages authentication for Streamlit applications that are integrated into Protean Platform.
    """

    is_logged_in: bool = False
    bearer_token: str = None

    def __init__(self, issuer_uri: str):
        self.issuer_uri = issuer_uri

    def authenticate(self) -> None:
        """Authenticates user using access token in the authorization header."""
        try:
            # Get JWKS from the provided issuer URI
            key_set = get_key_set(self.issuer_uri)

            # Get bearer token from authorization header
            self.bearer_token = get_bearer_token()

            # Decode and validate bearer token
            validate_bearer_token(self.bearer_token, key_set)

            # Mark authentication as successful if token validation did not fail
            self.is_logged_in = True

            # Store authentication status in the context store
            update_session_store(True)

        except Exception as e:
            raise Exception(f"Failed to authenticate: {e}")
