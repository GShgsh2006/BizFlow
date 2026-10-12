#生成token函数
import os
from datetime import datetime, timedelta, timezone

from jose import jwt
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")


def create_token(data:dict):

    data=data.copy()

    expire = datetime.now(timezone.utc) + timedelta(hours=2)

    data.update({
        "exp": expire
    })

    token = jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token