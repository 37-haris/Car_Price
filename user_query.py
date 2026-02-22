from sqlalchemy.orm import Session
from sqlalchemy import text


def get_all_users(db: Session):
    query = text("""
        SELECT id, name, lastname, email, phone, role
        FROM users
    """)
    result = db.execute(query).fetchall()

    return [
        {
            "id": row.id,
            "name": row.name,
            "lastname": row.lastname,
            "email": row.email,
            "phone": row.phone,
            "role": row.role
        }
        for row in result
    ]
    
def count_users(db: Session):
    query = text("""
        SELECT COUNT(*) AS user_count
        FROM users
    """)
    result = db.execute(query).fetchone()
    return result.user_count if result else 0

def get_all_normal_users(db: Session):
    query = text("""
        SELECT COUNT(*) AS user_count
        FROM users
        WHERE role = 'user'
    """)
    result = db.execute(query).fetchone()
    return result.user_count if result else 0

def get_all_admin_users(db: Session):
    query = text("""
        SELECT COUNT(*) AS user_count
        FROM users
        WHERE role = 'admin'
    """)
    result = db.execute(query).fetchone()
    return result.user_count if result else 0

    
def insert_user(db: Session, name: str, lastname: str, email: str, phone: str, password: str, role: str, bio: str):
    query = text("""
        INSERT INTO users (name, lastname, email, phone, password, role, bio)
        VALUES (:name, :lastname, :email, :phone, :password, :role, :bio)
    """)
    db.execute(query, {"name": name, "lastname": lastname, "email": email, "phone": phone, "password": password, "role": role, "bio": bio})
    db.commit()