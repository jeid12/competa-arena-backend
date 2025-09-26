from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.security import HTTPBearer
from config.db import init_db
from url.user_url import api_router



#env leading
load_dotenv()

#initialize an app
app=FastAPI()
#security schemes
bearer_scheme = HTTPBearer()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(api_router)   