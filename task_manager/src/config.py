from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/task_manager"
    echo_sql: bool = True
    test: bool = False
    project_name: str = "My FastAPI project"
    me_host: str = "0.0.0.0"
    me_port: int = 8001


settings = Settings()
