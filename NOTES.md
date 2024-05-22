## installations
pip install fastapi[all]
pip install psycopg[binary,pool]


### Auth Setting and Variables
secret_key: str
jwt_secret_key: str
jwt_refresh_secret_key: str
algorithm: str
REFRESH_TOKEN_EXPIRE_TIME: int 


### building & running docker-compose
docker-compose up --build