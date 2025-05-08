from typing import Type

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from fastpluggy.core.database import get_db
from fastpluggy.core.dependency import get_view_builder, get_fastpluggy
from fastpluggy.core.flash import FlashMessage
from fastpluggy.core.models_tools.sqlalchemy import ModelToolsSQLAlchemy
from fastpluggy.core.tools.fastapi import redirect_to_previous
from fastpluggy.core.view_builer.components.form import FormView
from fastpluggy.core.view_builer.components.list import ListButtonView
from fastpluggy.core.view_builer.components.model import ModelView
from fastpluggy.core.view_builer.components.table_model import TableModelView
from fastpluggy.fastpluggy import FastPluggy
from .crud import get_admin_instance
from ..crud_admin import CrudAdmin
from ..field_types.dynamic_fields import DynamicSelectFieldType
from ..schema import CrudAction

crud_api_router = APIRouter()

@crud_api_router.get("/dynamic-select/{model_name}/{field_name}")
async def dynamic_select_endpoint(
    model_name: str,
    field_name: str,
    value: str,
    request: Request,
    db: Session = Depends(get_db)
):
    model_class = ModelToolsSQLAlchemy.get_model_class(model_name)
    if model_class is None:
        return JSONResponse(status_code=404, content={"error": "Field not found"})

    admin = get_admin_instance(model_class.__name__)
    configured_fields = admin.configure_fields(CrudAction.CREATE)

    # Lookup the form field in a global registry
    field: DynamicSelectFieldType = configured_fields.get(field_name)

    if not field or not isinstance(field, DynamicSelectFieldType):
        return JSONResponse(status_code=404, content={"error": "Field not found"})

    # Execute the query factory with the value
    query = field.query_factory(value)
    results = db.execute(query)
    records = results.scalars().all()

    if isinstance(field.get_label, str):
        def get_value(obj):
            attr = getattr(obj, field.get_label, None)
            return attr() if callable(attr) else attr
    else:
        get_value = field.get_label

    return [{"id": obj.id, "name": get_value(obj)} for obj in records]
