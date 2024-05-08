import jwt, os, json
from typing import Dict, List
from models.models import User
from fastapi import HTTPException, Request

#secret key to encode jwt tokens and algorithm to use for creating jwt tokens
SECRET_KEY = os.environ.get('SECRET_KEY', 'SECRET-KEY')
ALGORITHM = "HS256"

def validate_token(request: Request, token: str):
    try:
        decoded_token: User = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        if not check_user_exists(decoded_token):
            raise HTTPException(status_code=404, detail='User not found.')
        
        request.state.userId = decoded_token['userId']
        request.state.username = decoded_token['username']
        request.state.firstName = decoded_token['firstName']
        request.state.lastName = decoded_token['lastName']
        request.state.metadata = decoded_token['metadata']

        return True
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=500,detail="Token Expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=500,detail="Invalid Token")

def create_token(user_info: Dict):
    try:
        if not check_user_exists(user_info):
            raise HTTPException(status_code=404, detail='User not found.')
        user_details = get_user_details_from_userId(user_info['userId'])
        token = jwt.encode(user_details, SECRET_KEY, ALGORITHM)
        return token
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail="Internal Server Error")

def check_user_exists(user_info: Dict[str, List[User]]):
    userId = user_info['userId']
    with open("database/static_users.json", "r") as f:
        users = json.load(f)
    return any([user.get('userId') == userId for user in users['USERS']])

def get_user_details_from_userId(userId: str):
    with open("database/static_users.json", "r") as f:
        users = json.load(f)
    return [user for user in users['USERS'] if user['userId'] == userId][0]