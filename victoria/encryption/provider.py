"""victoria.encryption.provider

Abstract base class of an encryption provider.

Author:
    Sam Gibson 
"""
from abc import ABC, abstractmethod
import os
from typing import Tuple, Optional, Union

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from .schemas import EncryptionEnvelope


class EncryptionProvider(ABC):
    """Abstract base class for an encryption provider. Provides methods
    for envelope encrypting/decrypting arbitrary byte/string sequences.
    """
    @abstractmethod
    def encrypt(self, data: bytes) -> EncryptionEnvelope:
        """Encrypt bytes to an EncryptionEnvelope.

        Args:
            data (bytes): The data to encrypt.

        Returns:
            EncryptionEnvelope: The encrypted data.
        """
        raise NotImplementedError()

    def encrypt_str(self,
                    data: str,
                    encoding: Optional[str] = "utf-8") -> EncryptionEnvelope:
        """Encrypt a string to an EncryptionEnvelope.

        Args:
            data (str): The string to encrypt.
            encoding (str, optional): The encoding of the data. Default utf-8.

        Returns:
            EncryptionEnvelope: The encrypted data.
        """
        return self.encrypt(data.encode(encoding))

    @abstractmethod
    def decrypt(self, envelope: EncryptionEnvelope) -> Union[bytes, None]:
        """Decrypt an EncryptionEnvelope to bytes.

        Please note that this can return None if the key encryption key
        is out of date.

        Args:
            envelope (EncryptionEnvelope): The envelope to decrypt.

        Returns:
            bytes: The decrypted data.
            None: If the key encryption key was out of date.
        """
        raise NotImplementedError()

    def decrypt_str(self,
                    envelope: EncryptionEnvelope,
                    encoding: Optional[str] = "utf-8") -> Union[str, None]:
        """Decrypt an EncryptionEnvelope to a string.

        Please note that this can return None if the key encryption key
        is out of date.

        Args:
            envelope (EncryptionEnvelope): The envelope to decrypt.
            encoding (str, optional): The encoding of the data. Default utf-8.

        Returns:
            str: The decrypted data.
            None: If the key encryption key was out of date.
        """
        decrypted = self.decrypt(envelope)
        if decrypted is None:
            return None
        return decrypted.decode(encoding)

    @abstractmethod
    def rotate_key(self,
                   envelope: EncryptionEnvelope,
                   version: Optional[str] = None) -> EncryptionEnvelope:
        """Rotate an EncryptionEnvelope encrypted with an old version of the
        key encryption key to a different version.

        Basically just decrypts it with the old key and reencrypts it with the 
        new key.

        Args:
            envelope (EncryptionEnvelope): The envelope to rotate.
            version (str, optional): The specific KEK version to use. Defaults
                to the latest if not given. You probably don't want to specify 
                this, as the latest will be the best version.
        
        Returns:
            EncryptionEnvelope: The newly rotated encrypted data.
        """
        raise NotImplementedError()

    def _data_encrypt(self, data: bytes) -> Tuple[bytes, bytes, bytes]:
        """Asymmetrically encrypt a piece of data, returning a tuple containing
        the encrypted data as a bytes object, the plaintext (!) encryption key 
        as a bytes object, and the nonce used to encrypt as a bytes object.

        Uses a 256-bit AES cipher in Galois Counter Mode, as recommended by 
        Google for generating data encryption keys: 
        https://cloud.google.com/kms/docs/envelope-encryption#data_encryption_keys

        Uses a 96-bit nonce length, as recommended by NIST for AES in GCM:
        https://csrc.nist.gov/publications/detail/sp/800-38d/final

        Args:
            data: The data to encrypt.

        Returns:
            Tuple:
                bytes: Encrypted data
                bytes: Plaintext (!) data encryption key -- encrypt with your 
                    key encryption key ASAP and do NOT store in plaintext!!
                bytes: 96-bit nonce value used with data encryption key when 
                    encrypting data. Under NO circumstances to be reused for
                    encryption with the same key.
        """
        key = AESGCM.generate_key(bit_length=256)
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)  # 12 bytes == 96 bits
        encrypted = aesgcm.encrypt(nonce, data, associated_data=None)
        return encrypted, key, nonce

    def _data_decrypt(self, data: bytes, key: bytes, nonce: bytes) -> bytes:
        """Decrypt a piece of data with its plaintext data encryption key, and
        its nonce.

        For more information on encryption, please see the '_data_encrypt()'
        function.

        Args:
            data: The data to decrypt.
            key: The plaintext (!) data encryption key.
            nonce: The nonce used to encrypt the data with the key.

        Returns:
            bytes: The decrypted data.
        """
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(nonce, data, associated_data=None)