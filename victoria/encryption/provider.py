from abc import ABC, abstractmethod
import os
from typing import Tuple

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from .schemas import EncryptionEnvelope


class EncryptionProvider(ABC):
    @abstractmethod
    def encrypt(self, data: bytes) -> EncryptionEnvelope:
        raise NotImplementedError()

    def encrypt_str(self,
                    data: str,
                    encoding: str = "utf-8") -> EncryptionEnvelope:
        return self.encrypt(data.encode(encoding))

    @abstractmethod
    def decrypt(self, envelope: EncryptionEnvelope) -> bytes:
        raise NotImplementedError()

    def decrypt_str(self,
                    envelope: EncryptionEnvelope,
                    encoding: str = "utf-8") -> str:
        return self.decrypt(envelope).decode(encoding)

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