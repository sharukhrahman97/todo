import os


class Settings:
    def __init__(self):
        self.DEBUG = os.getenv("DEBUG") == "True"

        self.ACCESS_TIMEOUT = os.getenv("ACCESS_TIMEOUT")
        self.REFRESH_TIMEOUT = os.getenv("REFRESH_TIMEOUT")
        self.SECRET = os.getenv("SECRET")
        
        self.PEPPER = os.getenv("PEPPER")

        self.POSTGRES_USER = os.getenv("POSTGRES_USER")
        self.POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
        self.POSTGRES_HOST = os.getenv("POSTGRES_HOST")
        self.POSTGRES_PORT = int(os.getenv("POSTGRES_PORT"))
        self.POSTGRES_DB = os.getenv("POSTGRES_DB")

        self.AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
        self.AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.AWS_REGION = os.getenv("AWS_REGION")

        self.MONGO_HOST = os.getenv("MONGO_HOST")
        self.MONGO_PORT = os.getenv("MONGO_PORT")

        self.REDIS_HOST = os.getenv("REDIS_HOST")
        self.REDIS_PORT = os.getenv("REDIS_PORT")
        
        self.SMTP_SERVER = os.getenv("SMTP_SERVER")
        self.SMTP_PORT = os.getenv("SMTP_PORT")
        self.SMTP_USERNAME = os.getenv("SMTP_USERNAME")
        self.SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

settings = Settings()
print(settings.__dict__)
