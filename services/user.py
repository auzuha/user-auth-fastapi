import json, uuid
from typing import List, Dict
from models.models import UserFilter, User
from models.api import CreateUserRequest, UpdateUserRequest
from fastapi import HTTPException
from database.failure_rollback import create_backup, rollback_on_failure
from services.file import dump_data_to_file

def get_users(filter: UserFilter = None) -> List[User]:
    with open("database/static_users.json", "r") as f:
        users = json.load(f)
    
    if not isinstance(filter, dict) and filter is not None:
        filter = filter.dict(exclude_none=True)
    
    user_list = [User(**user) for user in users["USERS"] if check_filter_conditions(user, filter)]
    return user_list

def create_user(user: User):
    if not user.userId:
        user.userId = str(uuid.uuid4())

    users = get_users()

    users.append(user)

    create_backup()

    dump_data_to_file(users)


def update_user(userId: str, updateUserRequest: UpdateUserRequest):
    
    user_to_update = get_users(filter=UserFilter(userId=userId))[0]

    update = updateUserRequest.update
    for key, value in update.items():
        if key in user_to_update.dict().keys():
            setattr(user_to_update, key, value)
            #user_to_update[key] = value
    
    users = get_users()
    
    for idx, user in enumerate(users):
        if user.userId == userId:
            users[idx] = user_to_update
            break
    
    create_backup()

    dump_data_to_file(users)
    
    return True

def delete_user(userId: str):
    does_user_exist = get_users(filter=UserFilter(userId=userId))
    if not does_user_exist:
        raise HTTPException(404, "User not found.")
    
    users = get_users()
    updated_users = [user for user in users if user.userId != userId]

    create_backup()

    dump_data_to_file(updated_users)
    
    return True
    
def create_user_validator(user: CreateUserRequest):
    print(type(user.userId))
    username = user.username
    user_with_same_userId_exists = get_users(filter=UserFilter(userId=user.userId))
    print(user_with_same_userId_exists)
    user_with_same_username_exists = get_users(filter=UserFilter(username=username))
    if user_with_same_username_exists:
        raise HTTPException(500,"Username already exists.")
    if user_with_same_userId_exists:
        raise HTTPException(500,"userId already exists.")
    return user

def update_user_validator(userId: str, updateUserRequest: UpdateUserRequest):
    user = get_users(filter=UserFilter(userId=userId))
    if not user:
        raise HTTPException(404, "User doesn't exist.")

    if "username" in updateUserRequest.update.keys():
        requested_username = updateUserRequest.update.get('username')
        user_with_same_username_exists = get_users(filter=UserFilter(username=requested_username))
        if user_with_same_username_exists:
            raise HTTPException(500,"Username already exists.")
    return updateUserRequest

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

