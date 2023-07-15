from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreateSchema, UserUpdateSchema

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreateSchema):
    db_user = User(username=user.username, email=user.email, password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: User, user_update: UserUpdateSchema):
    user.username = user_update.username
    user.email = user_update.email
    if user_update.password:
        user.password = get_password_hash(user_update.password)
    db.commit()
    return user
