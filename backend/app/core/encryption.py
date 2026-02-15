"""
Маълумотларни шифрлаш модули
AES-256 шифрлаш
"""
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os
from app.core.config import settings


class EncryptionService:
    """Шифрлаш сервиси"""
    
    def __init__(self):
        # Шифрлаш калитини яратиш
        key = settings.ENCRYPTION_KEY.encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'digital_service_salt',
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(key))
        self.cipher = Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """Маълумотни шифрлаш"""
        if isinstance(data, str):
            data = data.encode()
        encrypted = self.cipher.encrypt(data)
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Маълумотни дешифрлаш"""
        encrypted_data = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted = self.cipher.decrypt(encrypted_data)
        return decrypted.decode()


# Глобал шифрлаш сервиси
encryption_service = EncryptionService()
