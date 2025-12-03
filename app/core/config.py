import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT: str = os.getenv("MYSQL_PORT", "3306")
    MYSQL_DB: str = os.getenv("MYSQL_DB", "lmsdb")

    # MYSQL_USER: str = os.getenv("MYSQL_USER")
    # MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD")
    # MYSQL_HOST: str = os.getenv("MYSQL_HOST")
    # MYSQL_PORT: str = os.getenv("MYSQL_PORT")
    # MYSQL_DB: str = os.getenv("MYSQL_DB")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "BBDULMS")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_MINUTES: int = int(os.getenv("ACCESS_TOKEN_MINUTES", "30"))

    BASE_URL: str =os.getenv("BASE_URL")

    @property
    def database_url(self) -> str:
        # Encode password safely
        encoded_password = quote_plus(self.MYSQL_PASSWORD)
        return f"mysql+pymysql://{self.MYSQL_USER}:{encoded_password}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"


settings = Settings()
#print(settings.database_url)
