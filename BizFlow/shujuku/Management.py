from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from fastapi import HTTPException
import os
from pathlib import Path
from dotenv import load_dotenv
import logging
# 固定加载 BizFlow/.env（相对本文件向上两级），不依赖当前工作目录。
# override=True 让 .env 里的值覆盖同名系统变量（Windows 自带 USERNAME、
# 部分 shell 自带 HOSTNAME，否则会覆盖 MySQL 账号/主机导致连接失败）。
load_dotenv(r"D:\编程知识\编程知识\python\python项目\fastapixxxmmm\.env", override=True)
#数据库信息
import os

HOSTNAME = os.getenv("HOSTNAME")
PORT = os.getenv("PORT")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")

# 缺哪个就报哪个，一目了然
missing = [
    name for name, value in {
        "HOSTNAME": HOSTNAME,
        "PORT": PORT,
        "USERNAME": USERNAME,
        "PASSWORD": PASSWORD,
        "DATABASE": DATABASE,
    }.items()
    if not value
]

if missing:
    if missing:
        raise RuntimeError(f"环境变量缺失: {', '.join(missing)}，请检查 .env 文件")

db_url = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'
SQLALCHEMY_DATABASE_URI = db_url
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭不必要的警告
#创建数据库连接引擎
engine = create_engine(
    db_url,
    echo=False
)
# 3. 创建Session工厂
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)
#继承模型方便我们进行继承
class Base(DeclarativeBase):
    pass
#定义注入依赖的模板
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
