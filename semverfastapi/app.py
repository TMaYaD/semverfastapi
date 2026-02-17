from fastapi import FastAPI, APIRouter, Depends, Request
from fastapi.routing import APIRoute
from semverfastapi.core import Version # Updated import

def get_version_setter(version: str):
    async def set_version(request: Request):
        request.state.api_version = version
    return set_version

from semverfastapi.dependencies import check_api_version
from semverfastapi.core import Version, VersionedRoute

def VersionedApp(app: FastAPI, versions: list[str]) -> FastAPI:
    # 1. Capture original routes
    original_routes = list(app.routes)
    versioned_routes = []

    # 2. Clear app routes
    app.router.routes = []

    # 3. Add back ONLY unannotated routes (Global)
    for route in original_routes:
        versioned_route = VersionedRoute(route)
        if versioned_route.is_global():
            app.routes.append(route)
            continue

        versioned_routes.append(versioned_route)

        # Add unversioned route that redirects
        app.add_api_route(
            path=route.path,
            endpoint=route.endpoint,
            methods=route.methods,
            dependencies=[Depends(check_api_version)],
            include_in_schema=False,
            name=route.name
        )

    # 4. Now add versioned routers
    for version_str in versions:
         target_version = Version(version_str)
         # Add check_api_version to dependencies so it runs for every request to this router
         versioned_router = APIRouter(dependencies=[Depends(get_version_setter(version_str)), Depends(check_api_version)])

         # Use ORIGINAL routes to build versioned one
         for route in versioned_routes:

             route.add_to_router(versioned_router, target_version)

         app.include_router(versioned_router, prefix=f"/v{version_str}")

    return app
