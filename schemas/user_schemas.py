def user_serializer(user) -> dict:
  return {
    "id": str(user["_id"]),
    "email": user["email"],
    "password": user["password"],
    "type": user["type"]
  }

def users_serializer(users) -> list:
  return [user_serializer(user) for user in users]