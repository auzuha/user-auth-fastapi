from fastapi import APIRouter, Depends
from services.user import get_users, create_user_validator, create_user, update_user ,update_user_validator, delete_user
from models.api import GetUsersRequest, GetUsersResponse, CreateUserRequest, UpdateUserRequest, UpdateUserResponse

app = APIRouter(prefix='/api/users')


@app.post('/', response_model=GetUsersResponse)
def get_users_(getUsersRequest: GetUsersRequest):
    filter = getUsersRequest.filter

    results = get_users(filter=filter)
    return GetUsersResponse(results=results)

@app.post('/create')
def create_user_(createUserRequest: CreateUserRequest = Depends(create_user_validator)):
    try:
        create_user(createUserRequest)
        return createUserRequest
    except ValueError as e:
        print('asdad')

@app.patch('/{userId}', response_model=UpdateUserResponse)
def update_user_(userId: str, updateUserRequest: UpdateUserRequest = Depends(update_user_validator)):
    status = update_user(userId, updateUserRequest)
    return UpdateUserResponse(success=status)

@app.delete('/{userId}')
def delete_user_(userId: str):
    status = delete_user(userId=userId)
    return status