from passlib.context import CryptContext


def hash(password: str) -> str:
    """
    Hash a password using the bcrypt algorithm.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)
