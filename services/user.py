import json
from typing import List, Dict
from models.models import UserFilter, User

def get_users(filter: UserFilter) -> List[User]:
    with open("database/static_users.json", "r") as f:
        users = json.load(f)
    
    if not isinstance(filter, dict) and filter is not None:
        filter = filter.dict(exclude_none=True)
    
    user_list = [user for user in users["USERS"] if check_filter_conditions(user, filter)]
    return user_list

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

