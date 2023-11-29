from ninja import Router
from .api import router

event_router = Router()
event_router.add_router('/', router, tags=["event"])