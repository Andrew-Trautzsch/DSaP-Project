import hashlib
import json


# Password hashing and verification
def hashPassword(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def verifyPassword(password, hashed_password):
    return hashPassword(password) == hashed_password


def computeDataHash(data):
    # Normalize boolean and other data types for consistent representation
    serialized_data = json.dumps(data, sort_keys=True)
    return hashlib.sha256(serialized_data.encode("utf-8")).hexdigest()


def verifyDataHash(data, dataHash):
    return computeDataHash(data) == dataHash


def computeDatasetHash(dataSet):
    combinedData = "".join(data["data_hash"] for data in dataSet)
    return hashlib.sha256(combinedData.encode("utf-8")).hexdigest() 

