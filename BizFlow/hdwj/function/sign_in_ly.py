#BizFlow 智能业务协作平台
#登入和注册函数接口
#登入
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import Session
from fastapi import  HTTPException
from BizFlow.shujuku.user import users
from BizFlow.shujuku.yanzheng import verify_password,get_password_hash
import logging
from BizFlow.hdwj.tool.sc_token import create_token
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# 董事长注册验证码
CHAIRMAN_KEY = "zxcvbnm123456789"

def sign_in(name:str,password:str,db:Session):
    query_name=db.query(users).filter(users.name==name).first()
    if query_name:
        query_password=query_name.password
        yz=verify_password(password,str(query_password))

        if yz:
            zw=query_name.position
            token = create_token(
                {
                    "id": query_name.id,
                    "role": zw,
                    "Full_Name":name
                }
            )
            if zw=="董事长":
               logging.info("登入成功")
               return {"message": "欢迎董事长访问BizFlow智能业务协作平台",
                       "role": zw, "username": query_name.name,
                       "id": query_name.id, "token":token}
            else:
                logging.info("登入成功")

            return {"message": f"欢迎{zw}访问BizFlow智能业务协作平台",
                       "role": zw, "username": query_name.name,
                       "id": query_name.id, "token":token}
        else:
            raise HTTPException(status_code=401,detail="密码错误了！")
    else:
        raise HTTPException(status_code=401,detail="您还没有登入哦，赶快登入！！")

#注册接口
def sign_up(name:str,password:str,employee_id:int,position:str,db:Session):
    # 员工注册通道不允许直接注册成“董事长”，董事长必须走 /sign_up_yz 验证码通道
    if position == "董事长":
        raise HTTPException(status_code=403, detail="董事长账号请使用“注册董事长”通道并输入验证码")
    query_name=db.query(users).filter(users.name==name).first()
    query_gh=db.query(users).filter(users.employee_ID==employee_id).first()
    if not query_name and not query_gh :
        try:
            new_password = get_password_hash(password)
            post_rw=users(
                name=name,
                password=new_password,
                employee_ID=employee_id,
                position="员工",
            )
            db.add(post_rw)
            db.commit()
            logging.info("注册成功")
            return {"message": "注册成功欢迎你成为公司的一员",
                    "role": "员工", "username": name}
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=500,detail=f"错误原因是{e}")
    else:
        raise HTTPException(status_code=401,detail="该用户名或工号已经存在请重新注册")

#董事长验证接口：先校验验证码，再以“董事长”身份入库
def sign_yz(name:str,password:str,employee_id:int,position:str,yz:str,db:Session):
    if yz != CHAIRMAN_KEY:
        raise HTTPException(status_code=403, detail="密钥错误，你无权注册董事长")
    query_name = db.query(users).filter(users.name == name).first()
    query_gh = db.query(users).filter(users.employee_ID == employee_id).first()
    if not query_name and not query_gh:
        try:
            new_password = get_password_hash(password)
            post_rw = users(
                name=name,
                password=new_password,
                employee_ID=employee_id,
                position="董事长",
            )
            db.add(post_rw)
            db.commit()
            logging.info("注册成功")
            return {"message": "注册成功欢迎董事长",
                    "role": "董事长", "username": name}
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=500,detail=f"错误原因是{e}")
    else:
        raise HTTPException(status_code=401,detail="该用户名或工号已经存在请重新注册")
