from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/gateway"
    echo_sql: bool = True
    test: bool = False
    project_name: str = "My FastAPI project"
    oauth_token_secret: str = "2e4cbf153a977a63481dfbcba232479ab08bef31091cb04e19cb47573592c344"
    me_host: str = "0.0.0.0"
    me_port: int = 8000
    tm_host: str = "localhost"
    tm_port: int = 8001


settings = Settings()
