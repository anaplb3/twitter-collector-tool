import os
from dotenv import load_dotenv
from decouple import config

try:
    load_dotenv(dotenv_path=".env", verbose=True)
except:
    print("produção")

GLOBAL_CFG = {
    'consumer_key': config('consumerKey'),
    'consumer_secret': config('consumerSecret'),
    'bearer_token': config('bearerToken'),
    'access_token': config('accessToken'),
    'access_token_secret': config('accessTokenSecret'),
}


DEV_CFG = {
    "debug": True,
    "database_url": "postgresql://postgres:starwars@localhost/tweet-data",
    "sslmode": "disable",
    "port": 5000,
    "host": "127.0.0.1",
}

PROD_CFG = {
    "debug": False,
    "database_url": os.environ['DATABASE_URL'],
    "sslmode": "require",
    "port": int(os.environ.get("PORT", 5000)),
    "host": "0.0.0.0",

}