async def log_user(db, username, password):
    users = db["utilisateur"]
    user = users.find_one({"username": username})
    if user is not None and user["password"] == password:
        return {"success": True, "message": "Logged in successfully!", "user_id": user["_id"]}
    else:
        return {"success": False, "message": "Invalid username or password."}