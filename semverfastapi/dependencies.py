from fastapi import Request, Response, HTTPException
from fastapi.routing import APIRoute
from semverfastapi.core import Version, VersionedRoute # Updated import to package local

async def check_api_version(request: Request, response: Response):
    """
    Dependency to enforce version compatibility.
    """
    route = VersionedRoute(request.scope.get("route"))
    if route.is_global():
        return

    current_version = Version(getattr(request.state, "api_version", None))

    if not current_version:
        # Redirect to the introduced version
        new_path = f"/v{route.introduced}{request.url.path}"
        if request.url.query:
            new_path += f"?{request.url.query}"

        raise HTTPException(
            status_code=307,
            detail="Temporary Redirect",
            headers={"Location": new_path}
        )

    if route.is_removed_in(current_version):
        raise HTTPException(status_code=410, detail="Gone")

    if not route.is_available_in(current_version):
        raise HTTPException(
            status_code=426,
            detail="Upgrade Required",
            headers={"Upgrade": str(route.introduced)}
        )

    if route.is_deprecated_in(current_version):
        response.headers["Warning"] = "Deprecated API"
