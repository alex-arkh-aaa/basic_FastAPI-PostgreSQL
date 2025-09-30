from fastapi import FastAPI, responses, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db, create_tables
from . import crud
from .schemas import User, UserResponse
from contextlib import asynccontextmanager
from .security import *
from sqlalchemy import select



@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("✅ Таблицы созданы/проверены")
    yield



app = FastAPI(lifespan=lifespan)



# User endpoints
@app.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/", response_model=list[UserResponse])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_users(db, skip=skip, limit=limit)

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}


# @app.post("/users/", response_model=UserResponse)
# async def create_user(user: User, db: AsyncSession = Depends(get_db)):
#     return await crud.create_user(db, user.name, user.email, user.age)

@app.post("/register/")
async def register_user(user: User, db: AsyncSession = Depends(get_db)):
    existing_user = await crud.get_user_by_email(db, user.email)
    #existing_user = await db.execute(select(User).where(User.email == user.email))
    print(existing_user)
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    hashed_password = get_password_hash(user.password)
    new_user = await crud.create_user(db, user.name, user.email, user.age, hashed_password)

    return {"msg": "Пользователь успешно зарегистрирован", 'user': new_user}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app", host="127.0.0.1", port=8000, reload=True)
