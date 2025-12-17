from fastapi import FastAPI
from app.routes import users_route

app = FastAPI(title="FlexiPay", version='0.0.1', description='A modern, user-friendly Wallet and Savings app')

app.include_router(users_route.router)

@app.get('/')
def home():
    return {
        "message": "Welcome to FlexiPay"
    }