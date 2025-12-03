from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
MAX_BCRYPT_BYTES = 72


def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)

def hash_password(password: str):
    return pwd_context.hash(password[:MAX_BCRYPT_BYTES])

