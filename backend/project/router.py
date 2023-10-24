from ninja import Router
from .api import router

project_router = Router()
project_router.add_router('/', router, tags=["project"])