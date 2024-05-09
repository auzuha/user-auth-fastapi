import json, uuid
from typing import List, Dict
from models.models import UserFilter, User
from models.api import CreateUserRequest, UpdateUserRequest
from fastapi import HTTPException

def get_users(filter: UserFilter) -> List[User]:
    with open("database/static_users.json", "r") as f:
        users = json.load(f)
    
    if not isinstance(filter, dict) and filter is not None:
        filter = filter.dict(exclude_none=True)
    
    user_list = [User(**user) for user in users["USERS"] if check_filter_conditions(user, filter)]
    return user_list

def create_user(user: User):
    if not user.userId:
        user.userId = uuid.uuid4()
    user.userId = str(user.userId)
    
    with open('database/static_users.json', 'r') as f:
        users = json.load(f)
    users["USERS"].append(user.dict())

    with open('database/static_users.json', '+a') as f:
        json.dump(users,f,indent=4)


def update_user(userId: str, updateUserRequest: UpdateUserRequest):
    
    user_exists = get_users(filter=UserFilter(userId=userId))
    if not user_exists:
        raise HTTPException(404, "User doesn't exist.")
    user_to_update = user_exists[0].dict()
    update = updateUserRequest.update
    for key, value in update.items():
        if key in user_to_update.keys():
            user_to_update[key] = value
    
    with open('database/static_users.json', 'r') as f:
        users = json.load(f)
    
    for idx, user in enumerate(users["USERS"]):
        if user['userId'] == str(userId):
            users["USERS"][idx] = user_to_update
            break

    with open('database/static_users.json', 'w') as f:
        json.dump(users,f,indent=4)
    
    return True
    
def uniqueness_validator(user: CreateUserRequest):
    print(type(user.userId))
    username = user.username
    user_with_same_userId_exists = get_users(filter=UserFilter(userId=str(user.userId)))
    print(user_with_same_userId_exists)
    user_with_same_username_exists = get_users(filter=UserFilter(username=username))
    if user_with_same_username_exists:
        raise HTTPException(500,"Username already exists.")
    if user_with_same_userId_exists:
        raise HTTPException(500,"userId already exists.")
    return user

    
def check_filter_conditions(user: Dict, filter: Dict):
    if not filter:
        return True
    for key, value in filter.items():
        if value != user[key]:
            return False
    if filter.get('metadata'):
        if not user.get('metadata'):
            return False
        for key, value in filter['metadata'].items():
            if key not in user['metadata'].keys():
                return False
            if value != user['metadata'][key]:
                return False
            
    return True

