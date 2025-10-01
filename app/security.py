from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from config import settings

# Настраиваем контекст для хеширования паролей
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Функция для хеширования пароля
def get_password_hash(password):
    
    try:
        result = pwd_context.hash(password)
        print("✅ Хеширование успешно")
        return result
    except Exception as e:
        print(f"❌ Ошибка хеширования: {e}")
        raise

# Функция для проверки пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta = settings.ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})  # Добавляем время истечения
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None  # Если токен недействителен или истёк