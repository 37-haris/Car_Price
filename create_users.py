from main import SessionLocal, User, pwd_context

def create_users():
    db = SessionLocal()

    users = [
        {"name": "Haris", "email": "haris@example.com", "password": "123", "role": "user"},
        {"name": "Victorian", "email": "victorian@example.com", "password": "123", "role": "user"},
        {"name": "Stephane", "email": "stephane@example.com", "password": "123", "role": "user"},
        {"name": "Admin", "email": "admin@example.com", "password": "admin123", "role": "admin"},
    ]

    for u in users:
        # Remove old user if exists (to avoid malformed hash issues)
        existing_user = db.query(User).filter(User.email == u["email"]).first()
        if existing_user:
            db.delete(existing_user)
            db.commit()
            print(f"Removed old user {u['email']} with invalid hash")

        # Hash password properly with full Argon2 hash
        hashed_password = pwd_context.hash(u["password"][:72])
        user = User(
            name=u["name"],
            email=u["email"],
            password=hashed_password,
            role=u["role"]
        )
        db.add(user)
        print(f"Created user {u['email']} with valid Argon2 hash")

    db.commit()
    db.close()
    print("All test users inserted successfully with valid Argon2 hashes!")

if __name__ == "__main__":
    create_users()
