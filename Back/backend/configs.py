from dotenv import dotenv_values

venv = dotenv_values(".env")

#DATABASE
DATABASE_NAME = venv.get("DATABASE_NAME") 
USER_NAME = venv.get("DATABASE_USERNAME")
PASSWORD = venv.get("DATABASE_PASSWORD")
HOST = venv.get("HOST")
PORT = venv.get("PORT")

DATABASE_URL=f"""postgresql+psycopg2://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"""

#JWT
JWT_SECRET = venv.get("JWT_SECRET")
JWT_ALGORITHM = venv.get("JWT_ALGORITHM")
JWT_TOKEN_EXPIRE_MINUTES = venv.get("JWT_TOKEN_EXPIRE_MINUTES")

URL_API_LLM = venv.get("URL_API_LLM")