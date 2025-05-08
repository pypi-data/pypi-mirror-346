from typing import Type

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastpluggy.core.view_builer.components.list import ListButtonView
from fastpluggy.fastpluggy import FastPluggy
from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastpluggy.core.models_tools.sqlalchemy import ModelToolsSQLAlchemy
from .api import crud_api_router
from .crud import crud_view_router
from ..config import CrudConfig
from fastpluggy.core.auth import require_authentication
from fastpluggy.core.database import get_db
from fastpluggy.core.dependency import get_view_builder, get_fastpluggy
from fastpluggy.core.flash import FlashMessage
from fastpluggy.core.tools.fastapi import redirect_to_previous
from fastpluggy.core.tools.inspect_tools import get_module
from fastpluggy.core.view_builer.components.form import FormView
from fastpluggy.core.view_builer.components.model import ModelView
from fastpluggy.core.view_builer.components.table_model import TableModelView

from ..crud_admin import CrudAdmin
from ..schema import CrudAction

auth_dependencies = []
settings = CrudConfig()
if settings.require_authentication:
    auth_dependencies.append(Depends(require_authentication))

crud_router = APIRouter(dependencies=auth_dependencies)
crud_router.include_router(crud_view_router)
crud_router.include_router(crud_api_router)