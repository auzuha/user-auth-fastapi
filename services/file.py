import json
from typing import List
from models.models import User

def dump_data_to_file(usersList: List[User]):
    data = {
        "USERS" : [user.dict() for user in usersList]
    }
    with open('database/static_users.json', 'w') as f:
        json.dump(data, f, indent=4)