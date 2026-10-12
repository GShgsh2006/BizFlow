from BizFlow.shujuku.Management import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String,Index,Text
from sqlalchemy import DateTime
class users(Base):
   __tablename__ = 'user'
   id:Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
   name:Mapped[str] = mapped_column(String(200),unique=True)
   password:Mapped[str] = mapped_column(String(200))
   employee_ID:Mapped[int] = mapped_column(Integer,unique=True)#工号
   position:Mapped[str] = mapped_column(String(200))#职位

class task(Base):
   __tablename__ = 'task'
   id:Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
   name:Mapped[str] = mapped_column(String(200))#任务名称
   Deadline:Mapped[DateTime] = mapped_column(DateTime)#截止时间
   content:Mapped[str] = mapped_column(String(500))#内容
   assignor :Mapped[str] = mapped_column(String(500))#发布人
   assignee_id :Mapped[int] = mapped_column(Integer)#接收人
   status:Mapped[str] = mapped_column(String(200))#完成状态
   amount:Mapped[int] = mapped_column(Integer)#金额
#我们自己创造的表
class employees(Base):
   __tablename__ = 'employee'
   id:Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
   name:Mapped[str] = mapped_column(String(200))
   name_rw:Mapped[str] = mapped_column(String(200))
   content: Mapped[str] = mapped_column(String(500))  # 内容
   status: Mapped[str] = mapped_column(String(200))  # 完成状态
   progress:Mapped[int] = mapped_column(Integer)#完成进度


#员工提交表格
class yg_tjs(Base):
   __tablename__ = 'yg_tj'

   id:Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
   name:Mapped[str] = mapped_column(String(200))
   name_rw: Mapped[str] = mapped_column(String(200))
   content: Mapped[str] = mapped_column(String(500))
   assignee_id:Mapped[int] = mapped_column(Integer)
   zt:Mapped[str] = mapped_column(String(200))


#员工接收通知（已读未读表）
class notice(Base):
   __tablename__ = 'notice'
   id:Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
   name_id:Mapped[str] = mapped_column(String(200))#人物的id
   name:Mapped[str] = mapped_column(String(200))
   assignee:Mapped[str] = mapped_column(String(200))
   Read:Mapped[str] = mapped_column(String(200))


#员工年假表
class yynj(Base):
   __tablename__ = 'yynj'
   id:Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
   name:Mapped[str] = mapped_column(String(200))
   days:Mapped[int] = mapped_column(Integer)#请假天数

#优秀员工表
class yyygb(Base):
   __tablename__ = 'yyygb'
   id:Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
   name:Mapped[str] = mapped_column(String(200))

#ai记录表
class ai_jl(Base):
   __tablename__ = 'ai_jl'
   id:Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)#每条记录的id
   name_id:Mapped[str] = mapped_column(String(200))
   HumanMessage:Mapped[str] = mapped_column(Text)
   AIMessage:Mapped[str] = mapped_column(Text)
   __table_args__ = (
      Index("idx_name_id_id", "name_id", "id"),
   )
