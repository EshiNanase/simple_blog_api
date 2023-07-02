from sqlalchemy.orm import Session
from src.schemas.user import UserCreate
from src.models.models import User


def create_user_with_hashed_password(db: Session, user: UserCreate):

    hashed_password = user.password + 'hashed_badly'

    User.is_valid(db, user)

    user = User(
        email=user.email,
        username=user.username,
        password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_all_users(db: Session):
    return db.query(User).all()
