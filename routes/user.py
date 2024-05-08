from fastapi import APIRouter, Request
from services.user import get_users
from models.api import GetUsersRequest, GetUsersResponse

app = APIRouter(prefix='/api/users')


@app.post('/', response_model=GetUsersResponse)
def get_users_(getUsersRequest: GetUsersRequest):
    filter = getUsersRequest.filter

    results = get_users(filter=filter)
    return GetUsersResponse(results=results)

@app.post('/create')
def create_user_():
    pass

@app.patch('/{userId}')
def update_user_(userId: str):
    pass

@app.delete('/{userId}')
def delete_user_(userId: str):
    pass