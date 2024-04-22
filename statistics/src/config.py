from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = "My FastAPI project"
    me_host: str = "localhost"
    me_port: int = 8001
    kafka_host: str = "localhost"
    kafka_port: int = 9092
    kafka_topic_likes: str = "likes"
    kafka_topic_views: str = "views"
    ch_host: str = "localhost"
    ch_port: int = 9000


settings = Settings()
