import json


def rollback_on_failure():
    BACKUP_FILE_NAME = '_static_users_backup.json'
    backup = open('database/static_users.json', 'w')
    with open(f'database/{BACKUP_FILE_NAME}', 'r') as f:
        data = json.load(f)
        json.dump(data, backup, indent=4)
        backup.close()

def create_backup():
    BACKUP_FILE_NAME = '_static_users_backup.json'
    backup = open(f'database/{BACKUP_FILE_NAME}', 'w')
    with open('database/static_users.json', 'r') as f:
        data = json.load(f)
        json.dump(data, backup, indent=4)
        backup.close()
