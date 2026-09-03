from app.db.session import SessionLocal
from app.models.admin import Admin
from app.core.security import hash_password


def create_admin():
    db = SessionLocal()

    try:
        email = "admin@example.com"
        password = "Admin@1234"

        existing_admin = (
            db.query(Admin)
            .filter(Admin.email == email)
            .first()
        )

        if existing_admin:
            print("Admin already exists.")
            return

        admin = Admin(
            name="System Admin",
            email=email,
            hashed_password=hash_password(password),
            is_active=True,
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print("Admin created successfully.")
        print(f"Admin ID: {admin.admin_id}")
        print(f"Email: {admin.email}")

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()