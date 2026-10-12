from fastapi import FastAPI

from BizFlow.hdwj.Route.crud_Route import router
from BizFlow.hdwj.Route.sign_in_up import routers
from BizFlow.hdwj.Route.notice_ly import router_notice
from BizFlow.hdwj.Route.Salary_ly import router_gz


test_app = FastAPI()

test_app.include_router(router)
test_app.include_router(routers)
test_app.include_router(router_notice)
test_app.include_router(router_gz)