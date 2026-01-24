# Requirements

## Overview
`semverfastapi` provides Semantic Versioning support for FastAPI applications. It allows developers to decorate endpoints with version information (introduced, deprecated, removed) and automatically routes requests to the correct version based on the API version header.

## Features
- **Endpoint Versioning**: Mark endpoints with `@available(introduced="X.Y", deprecated="A.B", removed="C.D")`.
- **Automatic Routing**: The library handles routing requests to the appropriate handler based on the requested version.
- **Version Headers**: Expects headers or other mechanisms to specify the API version (implementation detail: middleware/dependency based).
- **Versioning Policy Enforcement**:
    - Returns `307 Temporary Redirect` if no version is specified (redirects to introduced version).
    - Returns `426 Upgrade Required` if a newer version is required.
    - Returns `410 Gone` if the feature is removed in the requested version.
    - Adds `Warning` header for deprecated endpoints.

## Non-Functional Requirements
- **Performance**: Minimal overhead on request routing.
- **Compatibility**: Compatible with FastAPI.
- **Ease of Use**: Simple decorator-based API.
