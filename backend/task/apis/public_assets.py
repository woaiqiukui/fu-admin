from typing import List
from ninja import Router, ModelSchema, Query, Field
from ninja.pagination import paginate

from task.models import PublicAsset
from utils.fu_crud import create, delete, update, retrieve, ImportSchema, export_data, import_data
from utils.fu_ninja import FuFilters, MyPagination

router = Router()

# 设置过滤字段
class Filters(FuFilters):
    name: str = Field(None, alias="asset_name")
    root_domain_or_ip: str = Field(None, alias="root_domain_or_ip")
    company_name: str = Field(None, alias="company_name")
    additional_info: str = Field(None, alias="additional_info")
    project_id: str = Field(None, alias="project_id")

# 设置请求接收字段
class PublicAssetSchemaIn(ModelSchema):
    asset_name: str = Field(..., alias="asset_name")
    root_domain_or_ip: str = Field(..., alias="root_domain_or_ip")
    company_name: str = Field(..., alias="company_name")
    additional_info: str = Field(None, alias="additional_info")
    project_id: int = Field(..., alias="project_id")

    class Config:
        model = PublicAsset
        model_fields = ['asset_name', 'root_domain_or_ip', 'company_name', 'additional_info', 'project_id']

# 设置响应字段
class PublicAssetSchemaOut(ModelSchema):
    class Config:
        model = PublicAsset
        model_fields = "__all__"

# 创建PublicAsset
@router.post("/public_assets", response=PublicAssetSchemaOut)
def create_demo(request, data: PublicAssetSchemaIn):
    public_asset = create(request, data, PublicAsset)
    return public_asset

# 删除PublicAsset
@router.delete("/public_assets/{public_asset_id}")
def delete_demo(request, public_asset_id: int):
    delete(public_asset_id, PublicAsset)
    return {"success": True}

# 更新PublicAsset
@router.put("/public_assets/{public_asset_id}", response=PublicAssetSchemaOut)
def update_demo(request, public_asset_id: int, data: PublicAssetSchemaIn):
    public_asset = update(request, public_asset_id, data, PublicAsset)
    return public_asset

# 获取PublicAsset List
@router.get("/public_assets", response=List[PublicAssetSchemaOut])
@paginate(MyPagination)
def get_demo_list(request, filters: Filters = Query(...)):
    return retrieve(request, PublicAsset, filters)

