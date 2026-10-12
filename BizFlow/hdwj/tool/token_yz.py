#验证token检查是否登入
from fastapi import  Request
from fastapi.responses import JSONResponse
SECRET_KEY = "secret"
ALGORITHM = "HS256"

PUBLIC_PATHS = {
    "/sign_in",
    "/sign_up",
    "/sign_up_yz",
    "/docs",
    "/openapi.json",
    "/redoc",
    "/favicon.ico",
}

async def auth_middleware(request: Request, call_next):
    # 预检请求
    if request.method == "OPTIONS":
        return await call_next(request)

    if request.url.path in PUBLIC_PATHS:
        return await call_next(request)

    auth = request.headers.get("Authorization")
    token = auth.split(" ")[1] if auth and auth.startswith("Bearer ") else None

    if not token:
        return JSONResponse(status_code=401, content={"detail": "未登录，请先登录"})
    return await call_next(request)