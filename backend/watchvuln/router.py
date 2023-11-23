from ninja import Router
from .api import router

watchvuln_router = Router()
watchvuln_router.add_router('/', router, tags=["watchvuln"])