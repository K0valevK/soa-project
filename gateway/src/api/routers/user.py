from api.auth.oauth import oauth2_scheme, SECRET_KEY, ALGORITHM
from crud.user import get_user, create_user, fill_info
from database import get_db_session
from grpc_client import get_stub
from schemas.user import User, UserCreate, UserUpdate, UserResponse
from schemas.token import DataToken, Token
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt, JWTError
from typing import Annotated

from protos.task_manager_pb2_grpc import TaskManagerServerStub
from protos.task_manager_pb2 import CreateUserRequest, CreateTaskResponse
from google.protobuf.json_format import MessageToDict

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_db_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login: str = payload.get("sub")
        if login is None:
            raise credentials_exception
        token_data = DataToken(login=login)
    except JWTError:
        raise credentials_exception
    user = await get_user(db, token_data.login)
    if user is None:
        raise credentials_exception
    return user


@router.post("/signup", response_model=UserResponse)
async def new_user(user: UserCreate,
                   db: AsyncSession = Depends(get_db_session),
                   stub: TaskManagerServerStub = Depends(get_stub)):
    db_user = await get_user(db, user.login)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Login already exists")

    resp = await stub.CreateUser(CreateUserRequest(login=user.login))

    result = await create_user(db, user)
    return UserResponse(login=result.login,
                        first_name=result.first_name,
                        last_name=result.last_name,
                        birth_date=result.birth_date,
                        email=result.email,
                        phone_num=result.phone_num)


@router.put("", response_model=UserResponse)
async def upd_user(args: UserUpdate,
                   current_user: User = Depends(get_current_user),
                   db: AsyncSession = Depends(get_db_session)):
    db_user = await get_user(db, current_user.login)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    result = await fill_info(db, current_user.login, args)
    return UserResponse(login=result.login,
                        first_name=result.first_name,
                        last_name=result.last_name,
                        birth_date=result.birth_date,
                        email=result.email,
                        phone_num=result.phone_num)


'''
@router.get("/{user_login}", response_model=User)
async def user_details(user_login: str, db: AsyncSession = Depends(get_db_session)):
    result = await get_user(db, user_login)
    return result
'''
