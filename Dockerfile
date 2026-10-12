# 1. 使用官方的 Python 3.12 精简版作为基础镜像
FROM python:3.12-slim

# 2. 设置工作目录
WORKDIR /app

# 3. 先复制依赖清单，利用 Docker 缓存加速
COPY requirements.txt .

# 4. 安装依赖（使用清华源加速，避免超时）
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 5. 复制项目其余代码
COPY . .

# 6. 暴露端口
EXPOSE 8000

# 7. 启动命令 (⚠️注意确认)
CMD ["uvicorn", "BizFlow.hdwj.app:app", "--host", "0.0.0.0", "--port", "8000"]