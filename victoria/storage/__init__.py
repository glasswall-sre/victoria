import logging

from . import provider, azure_provider, local_provider

StorageProvider = provider.StorageProvider

PROVIDERS_MAP = {
    "azure": azure_provider.AzureStorageProvider,
    "local": local_provider.LocalStorageProvider
}


def make_provider(provider_type: str, **kwargs) -> provider.StorageProvider:
    try:
        return PROVIDERS_MAP[provider_type](**kwargs)
    except KeyError:
        logging.error(f"Invalid storage provider type '{provider_type}'")