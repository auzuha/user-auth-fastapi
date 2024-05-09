import json
from typing import List
from models.models import User
from database.failure_rollback import create_backup, rollback_on_failure
from fastapi import HTTPException

def dump_data_to_file(usersList: List[User]):
    try:
        create_backup()

        data = {
            "USERS" : [user.dict() for user in usersList]
        }
        with open('database/static_users.json', 'w') as f:
            json.dump(data, f, indent=4)
    except:
        print('rollback triggered!')
        rollback_on_failure()
        raise HTTPException(500,"Database update failed. Changes not reflected")