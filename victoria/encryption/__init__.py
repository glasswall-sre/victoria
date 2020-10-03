"""victoria.encryption

Package providing encryption functionality for Victoria.

Author:
    Sam Gibson 
"""
import logging

from . import provider, azure_provider
from .schemas import EncryptionProviderConfigSchema, EncryptionProviderConfig

EncryptionProvider = provider.EncryptionProvider

PROVIDERS_MAP = {"azure": azure_provider.AzureEncryptionProvider}
"""Map provider names to implementations. Used in make_provider() factory
function."""


def make_provider(provider_type: str, **kwargs) -> provider.EncryptionProvider:
    """Make an EncryptionProvider from a provider type. Call with the arguments
    you would normally provide to the specific implementation's constructor.

    make_provider("azure", vault_url="...", ...)

    Args:
        provider_type (str): The type of the provider. See PROVIDERS_MAP.
        **kwargs: The arguments for the provider implementation's constructor.

    Returns:
        EncryptionProvider: The provider of the given type.

    Raises:
        ValueError: If provider_type was invalid (i.e. not in PROVIDERS_MAP).
        TypeError: If the wrong arguments were given in kwargs.
    """
    try:
        return PROVIDERS_MAP[provider_type](**kwargs)
    except KeyError as err:
        raise ValueError(f"Invalid encryption provider_type '{provider_type}'") from err
