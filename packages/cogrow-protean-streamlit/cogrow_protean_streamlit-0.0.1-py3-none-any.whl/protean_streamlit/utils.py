from typing import Any

import requests
import streamlit as st
from joserfc import jwt
from joserfc.errors import JoseError
from joserfc.jwk import KeySet
from joserfc.rfc7519.registry import JWTClaimsRegistry


@st.cache_resource(ttl="1d")
def get_key_set(issuer_uri: str) -> KeySet:
    jwks = get_jwks(issuer_uri)
    return KeySet.import_key_set(jwks)


def get_jwks(issuer_uri: str) -> Any:
    """Get JWKS for the provided issuer URL."""
    try:
        jwks_uri = get_jwks_uri(issuer_uri)
        jwks = requests.get(jwks_uri)
        jwks.raise_for_status()
        return jwks.json()
    except Exception as e:
        raise Exception(f"Failed to fetch JWKS: {e}")


def get_jwks_uri(issuer_uri: str) -> str:
    """Get JWKS URL from OIDC discovery endpoint."""
    try:
        discovery_url = f"{issuer_uri.rstrip('/')}/.well-known/openid-configuration"
        resp = requests.get(discovery_url)
        resp.raise_for_status()
        metadata = resp.json()
        jwks_uri = metadata.get("jwks_uri")
        if not jwks_uri:
            raise Exception("JWKS URI not found in issuer metadata.")
        return jwks_uri
    except Exception as e:
        raise Exception(f"Failed to fetch JWKS URI from OIDC discovery endpoint: {e}")


def get_bearer_token() -> str:
    """Retrieve bearer token from authorization header."""
    authorization_header = get_header("Authorization")

    if not authorization_header.startswith("Bearer "):
        raise Exception("Bearer token is not present in authorization header.")

    access_token = authorization_header.split(" ")[1]
    if not access_token:
        raise Exception("Bearer token not present in Authorization header.")

    return access_token


def get_header(header_name: str) -> str | None:
    """Retrieve value from the requested header."""
    try:
        return st.context.headers[header_name]
    except KeyError:
        raise Exception(f"{header_name} header is not present.")


def validate_bearer_token(bearer_token: str, key_set: KeySet) -> None:
    """Validate bearer token signature and expiration."""
    try:
        # Decode and validate token signature
        decoded_bearer_token = jwt.decode(bearer_token, key_set)
        # Validate token claims
        JWTClaimsRegistry().validate(decoded_bearer_token.claims)
    except JoseError as e:
        raise Exception(e.description)
    except Exception as e:
        raise Exception(f"Access token validation failed. {e}")


def update_session_store(authentication_status: bool) -> None:
    """Update session store with the authentication information."""
    st.session_state["authentication_status"] = authentication_status


def get_authentication_status() -> bool:
    authentication_status = st.session_state.get("authentication_status")
    if not authentication_status:
        return False
    return st.session_state.get("authentication_status")
