# Authentication code will be added later.


from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

# Load Environment Variables
load_dotenv()

# ==========================
# Password Encryption
# ==========================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# ==========================
# JWT Configuration
# ==========================

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
)

# ==========================
# Hash Password
# ==========================

def hash_password(password: str):
    # bcrypt supports maximum 72 bytes
    password = password[:72]
    return pwd_context.hash(password)

# ==========================
# Verify Password
# ==========================

def verify_password(plain_password: str, hashed_password: str):
    plain_password = plain_password[:72]

    return pwd_context.verify(
        plain_password,
        hashed_password
    )

# ==========================
# Create JWT Token
# ==========================

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

# ==========================
# Decode JWT Token
# ==========================

def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None