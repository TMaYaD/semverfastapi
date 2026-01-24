# Architecture

## Core Components

### 1. `decorators.py`
Contains the `@available` decorator. This decorator attaches metadata (`_api_version_intro`, `_api_version_depr`, `_api_version_rem`) to the endpoint function. This metadata is later used by the routing logic to decide if an endpoint should be included in a specific API version.

### 2. `core.py`
Defines the `Version` class. This class handles parsing semantic version strings (e.g., "1.0", "2.1") and supports comparison operators (`<`, `>`, `<=`, `>=`). This is essential for determining if a requested version falls within the availability range of an endpoint.

### 3. `app.py`
Contains the `VersionedApp` factory function.
- It iterates over a list of supported versions.
- For each version, it creates a new `APIRouter`.
- It iterates over all original routes in the FastAPI app.
- It checks the `@available` metadata of each route's endpoint.
- It filters routes based on the current version loop (e.g., if version is "1.0", it includes routes introduced <= "1.0" and not removed <= "1.0").
- It mounts these versioned routers (e.g., `/v1.0`, `/v2.0`).

### 4. `dependencies.py`
Provides `check_api_version` dependency.
- Checks the `X-API-Version` header (or equivalent state).
- Compares the requested version with the endpoint's metadata.
- Raises appropriate HTTP exceptions (`307`, `426`, `410`) or adds headers (`Warning`) based on the comparison.

## Data Flow
1. Developer defines endpoints and marks them with `@available`.
2. `VersionedApp` is called with the FastAPI app and list of versions.
3. `VersionedApp` constructs the routing table for each version.
4. Incoming request hits a versioned route (e.g., `/v1.0/items`).
5. (Implicitly) Middleware or Dependency sets `request.state.api_version`.
6. Use of `check_api_version` dependency (if manually added or globally enforced) ensures the request matches the specific endpoint constraints, though `VersionedApp`'s routing structure already enforces existence. *Note: `dependencies.py` seems to be designed for finer-grained control or specific middleware usage patterns.*
