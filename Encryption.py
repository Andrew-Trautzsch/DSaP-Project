from cryptography.fernet import Fernet, InvalidToken

# Load or generate encryption key
KEY_FILE = "EncryptionKey.key"


def loadKey():
    """Load the encryption key from a file, or create a new one if it doesn't exist."""
    try:
        with open(KEY_FILE, "rb") as keyFile:
            return keyFile.read()
    except FileNotFoundError:
        # Generate a new key and save it to the file
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as keyFile:
            keyFile.write(key)
        return key


# Load or generate the encryption key
ENCRYPTION_KEY = loadKey()
fernet = Fernet(ENCRYPTION_KEY)


def encryptData(data):
    """Encrypt a value using Fernet encryption."""
    return fernet.encrypt(str(data).encode()).decode()


def decryptData(encryptedData):
    """Decrypt data only if it is encrypted."""
    try:
        return fernet.decrypt(encryptedData.encode()).decode()
    except (InvalidToken, AttributeError):
        # Return the data as-is if it's not encrypted
        return encryptedData