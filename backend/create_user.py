#!/usr/bin/env python3
"""
Create a user from the command line for the project.
Run from the repository root as: `python backend/create_user.py ...`
"""
import argparse
from getpass import getpass
from sqlalchemy import or_

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole


def parse_args():
    p = argparse.ArgumentParser(description="Create a user in the database")
    p.add_argument("--username", required=True, help="Username")
    p.add_argument("--email", required=True, help="Email")
    p.add_argument("--full-name", dest="full_name", required=True, help="Full name")
    p.add_argument("--role", default="analyst", help="Role (admin, tax_inspector, analyst, business_owner)")
    p.add_argument("--password", help="Password (if omitted, will prompt)")
    p.add_argument("--is-superuser", action="store_true", help="Mark user as superuser")
    return p.parse_args()


def main():
    args = parse_args()

    password = args.password or getpass("Password: ")
    if not password:
        print("Password is required")
        return

    session = SessionLocal()
    try:
        # Check existing user by username or email
        existing = session.query(User).filter(or_(User.username == args.username, User.email == args.email)).first()
        if existing:
            print(f"User with username or email already exists: {existing.username} <{existing.email}>")
            return

        # Validate role
        try:
            role_enum = UserRole(args.role)
        except ValueError:
            print("Invalid role. Available roles:")
            for r in UserRole:
                print(f" - {r.value}")
            return

        hashed = get_password_hash(password)

        user = User(
            username=args.username,
            email=args.email,
            full_name=args.full_name,
            role=role_enum,
            hashed_password=hashed,
            is_superuser=args.is_superuser,
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        print(f"Created user: id={user.id} username={user.username} role={user.role.value}")
    except Exception as e:
        session.rollback()
        print("Error creating user:", e)
    finally:
        session.close()


if __name__ == "__main__":
    main()
