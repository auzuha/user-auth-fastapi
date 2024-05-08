from fastapi import APIRouter, Request

app = APIRouter(prefix='/api/users')


@app.get('/')
def get_users(request: Request):
    return True