from fastapi import APIRouter
from app.routers.proxy import proxy_router
from app.routers.api import api_router

routers: list[APIRouter] = [proxy_router, api_router]
