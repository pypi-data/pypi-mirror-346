"""
Streamlit SDK for the Protean platform
"""

from .protean_authenticator import ProteanAuthenticator
from .utils import get_authentication_status

__all__ = [
    "ProteanAuthenticator",
    "get_authentication_status",
]
__version__ = "0.0.1"
