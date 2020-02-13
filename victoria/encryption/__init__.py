import logging

from . import provider, azure_provider
from .schemas import EncryptionProviderConfigSchema, EncryptionProviderConfig

EncryptionProvider = provider.EncryptionProvider

PROVIDERS_MAP = {"azure": azure_provider.AzureEncryptionProvider}


def make_provider(provider_type: str, **kwargs) -> provider.EncryptionProvider:
    try:
        return PROVIDERS_MAP[provider_type](**kwargs)
    except KeyError:
        logging.error(f"Invalid encryption provider type '{provider_type}'")