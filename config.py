from pydantic import BaseSettings

class Config(BaseSettings):
    bot_token: str
    admin_ids: list[int]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

def load_config():
    return Config(_env_file=".env")