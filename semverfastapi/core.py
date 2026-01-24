from typing import Optional

class Version:
    def __init__(self, v_str: Optional[str]):
        self.v_str = v_str
        if v_str is None:
            self.major = None
            self.minor = None
            return

        try:
            parts = v_str.split('.')
            self.major = int(parts[0])
            self.minor = int(parts[1]) if len(parts) > 1 else 0
        except:
            self.major = 0
            self.minor = 0

    def __bool__(self):
        return self.v_str is not None

    def __ge__(self, other):
        if not self or not other:
            return False
        return (self.major, self.minor) >= (other.major, other.minor)

    def __gt__(self, other):
        if not self or not other:
            return False
        return (self.major, self.minor) > (other.major, other.minor)

    def __le__(self, other):
        if not self or not other:
            return False
        return (self.major, self.minor) <= (other.major, other.minor)

    def __str__(self):
        return self.v_str if self.v_str is not None else "None"

from fastapi.routing import APIRoute, APIRouter

class VersionedRoute:
    def __init__(self, route: APIRoute):
        self.route = route
        self.endpoint = getattr(route, "endpoint", None)
        self.introduced = Version(getattr(self.endpoint, "_api_version_intro", None))
        self.deprecated = Version(getattr(self.endpoint, "_api_version_depr", None))
        self.removed = Version(getattr(self.endpoint, "_api_version_rem", None))

    def is_global(self) -> bool:
        return not self.introduced

    def is_available_in(self, version: Version) -> bool:
        if not self.introduced:
            # If not explicitly introduced, assume it's available?
            # In current logic, we filter out non-introduced routes before creating VersionedRoute logic in loop.
            # But safe default:
            return True

        if version < self.introduced:
            return False

        if self.is_removed_in(version):
            return False

        return True

    def is_removed_in(self, version: Version) -> bool:
        return self.removed and version >= self.removed

    def is_deprecated_in(self, version: Version) -> bool:
        return self.deprecated and version >= self.deprecated

    def add_to_router(self, router: APIRouter, version: Version):
        is_available = self.is_available_in(version)
        is_deprecated = self.is_deprecated_in(version)

        router.add_api_route(
            path=self.route.path,
            endpoint=self.route.endpoint,
            methods=self.route.methods,
            name=self.route.name,
            include_in_schema=self.route.include_in_schema and is_available,
            response_model=self.route.response_model,
            summary=self.route.summary,
            description=self.route.description,
            tags=self.route.tags + [f"v{version}"] if version else self.route.tags,
            dependencies=self.route.dependencies,
            deprecated=self.route.deprecated or is_deprecated,
            status_code=self.route.status_code,
            response_class=self.route.response_class,
            response_model_include=self.route.response_model_include,
            response_model_exclude=self.route.response_model_exclude,
            response_model_by_alias=self.route.response_model_by_alias,
            response_model_exclude_unset=self.route.response_model_exclude_unset,
            response_model_exclude_defaults=self.route.response_model_exclude_defaults,
            response_model_exclude_none=self.route.response_model_exclude_none,
            operation_id=self.route.operation_id
        )
