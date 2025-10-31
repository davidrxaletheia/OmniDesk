from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 3306
    DATABASE_USER: str
    DATABASE_PASSWORD: str = ""
    DATABASE_NAME: str

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXP_SECONDS: int = 3600
    # Development helper: allow fallback when token 'iat' claim is slightly in
    # the future due to clock skew. Set to False in production.
    JWT_LEEWAY_SECONDS: int = 5
    JWT_ALLOW_IAT_FALLBACK: bool = False

    # Discount applied to premium clients (fractional, e.g. 0.10 = 10%)
    PREMIUM_DISCOUNT_PCT: float = 0.10

    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
