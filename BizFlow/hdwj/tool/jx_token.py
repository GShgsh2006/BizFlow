from fastapi import Header,HTTPException
from jose import jwt

import os
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")


def get_current_user(
    #默认值给空串：不然不带 Authorization 头时 FastAPI 直接抛 422，
    #前端拿不到 401 就不会跳登录页（http.js 的拦截器只认 401）。
    authorization: str = Header(default="")
):

    try:

        token = authorization.split(" ")[1]


        data=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )


        return data


    except:
        raise HTTPException(
            status_code=401,
            detail="token无效"
        )