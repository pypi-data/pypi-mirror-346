from fastapi import APIRouter, Request, Depends

from fastpluggy.core.dependency import get_view_builder, get_fastpluggy
from fastpluggy.core.menu.decorator import menu_entry

crud_admin_view_router = APIRouter(prefix='/models', tags=["front_action"])


@menu_entry(type='admin')
@crud_admin_view_router.api_route("", methods=["GET", "POST"], name="crud_list")
async def list_models(request: Request, view_builder=Depends(get_view_builder),
                      fast_pluggy=Depends(get_fastpluggy)):

    items = []


    return view_builder.generate(
        request,
        title="List of models",
        items=items,
    )

