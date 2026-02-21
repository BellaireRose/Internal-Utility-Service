import config

def get_users():
    # Fake database simulation
    return [
        {
            "id": 1,
            "name": "Alice",
            "db_user": config.DB_USER  #leaking credentials
        },
        {
            "id": 2,
            "name": "Bob",
            "db_password": config.DB_PASSWORD  #leaking password
        }
    ]
