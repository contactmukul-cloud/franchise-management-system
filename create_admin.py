from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import hash_password

db = SessionLocal()

existing_admin = db.query(User).filter(User.email == "admin@gmail.com").first()

if existing_admin:
    print("Admin already exists")
else:
    admin = User(
        name="Admin",
        email="admin@gmail.com",
        password_hash=hash_password("admin123"),
        phone="9999999999",
        address="Head Office",
        role="super_admin",
        is_active=True,
        is_verified=True
    )

    db.add(admin)
    db.commit()
    print("Super Admin Created Successfully")

db.close()