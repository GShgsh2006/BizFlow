#BizFlow 智能业务协作平台
#中间件文件


import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fastapi")


# 1. 定义一个中间件类，继承自 BaseHTTPMiddleware
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 请求到达时：记录开始时间
        start_time = time.time()
        logger.info(f"【中间件拦截】收到请求: {request.method} {request.url.path}")

        # 调用下一个中间件或具体的路由函数（放行）
        response = await call_next(request)

        # 响应返回前：计算耗时并记录日志
        process_time = time.time() - start_time
        logger.info(f"【中间件放行】请求处理完成 | 状态码: {response.status_code} | 耗时: {process_time:.4f}秒")

        return response