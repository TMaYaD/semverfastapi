# SemVerFastAPI

A library for Semantic Versioning in FastAPI applications.

## Usage

```python
from fastapi import FastAPI
from semverfastapi import VersionedApp, available

app = FastAPI()

@app.get("/items")
@available(introduced="1.0", deprecated="1.1", removed="2.0")
def get_items():
    return [{"name": "Item 1"}]

@app.get("/items")
@available(introduced="2.1")
def get_items_v2():
    return [{"name": "Item 2"}]

app = VersionedApp(app, versions=["1.0", "1.1", "2.0", "2.1"])
```
