from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
DB_USER = os.getenv("DB_USER") 
DB_HOST = os.getenv("DB_HOST") 
DB_PASS = os.getenv("DB_PASS") 
DB_PORT = os.getenv("DB_PORT") 