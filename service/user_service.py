import re
from uuid import uuid4

from fastapi import HTTPException, Request
from peewee import DoesNotExist
from werkzeug.security import generate_password_hash, check_password_hash

from database import objects
from models import User, Session


def validate_password(password: str):
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
    if not re.search('[A-Z]', password):
        raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter")
    if not re.search('[0-9]', password):
        raise HTTPException(status_code=400, detail="Password must contain at least one digit")


async def registration(login: str, email: str, password: str, password_confirm: str):
    if await objects.count(User.select().where(User.login == login)) > 0:
        raise HTTPException(status_code=409, detail="Login already exists")

    if password != password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    validate_password(password)

    user = await objects.create(
        User,
        login=login,
        email=email,
        role=1,
        password=generate_password_hash(password)
    )
    user = await objects.get_or_none(User.select().where(User.id == user.id))
    return user.get_dto()


async def authorization(login: str, password: str):
    try:
        user = await objects.get(User.select().where(User.login == login))
    except DoesNotExist:
        raise HTTPException(status_code=400, detail="Wrong login")

    if not check_password_hash(user.password, password):
        raise HTTPException(status_code=400, detail="Wrong password")

    user_sessions = await objects.execute(Session.select().where(Session.user == user))

    if len(user_sessions) >= 5:
        oldest_session = min(user_sessions, key=lambda session: session.id)
        await objects.delete(oldest_session)

    session = await objects.create(Session, user=user, session=str(uuid4()))
    return user.get_dto(), session.session


async def authorization_check(session: str):
    sessions = await objects.execute(Session.select().where(Session.session == session))
    if len(sessions) <= 0:
        raise HTTPException(status_code=401, detail="Unauthorized")
    session = sessions[0]

    users = await objects.execute(User.select().where(User.id == session.user))
    if not users:
        raise HTTPException(status_code=403, detail="Forbidden")

    return users[0].get_dto()


async def get_current_user(request: Request):
    user_session = request.cookies.get('session')
    if not user_session:
        raise HTTPException(status_code=401, detail="Unauthorized")

    session = await objects.get(Session.select().where(Session.session == user_session))
    if session is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = await objects.get(User.select().where(User.id == session.user))
    return user


# async def change_password(user_id: int, password: str):
#     user = await objects.get_or_none(User.select().where(User.id == user_id))
#     if not user:
#         raise HTTPException(status_code=400, detail="User not found")
#     validate_password(password)
#     user.password = generate_password_hash(password)
#     await objects.update(user)


async def get_users():
    users = await objects.execute(User.select())
    return [user.get_dto() for user in users]


async def get_user(user_id: int):
    user = await objects.get_or_none(User.select().where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    return user.get_dto()

