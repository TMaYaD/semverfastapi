# Testing

## Prerequisites
- Python 3.9+
- `pytest`

## Running Tests
To run the full test suite, execute:
```bash
pytest
```

## Test Structure
- `tests/test_core.py`: Unit tests for version parsing and comparison.
- `tests/test_decorators.py`: Verification of metadata attachment.
- `tests/test_dependencies.py`: Tests for the dependency logic (exceptions and headers).
- `tests/test_app.py`: Integration tests verifying correct routing and 404s for versioned/non-versioned paths.

## Writing Tests
- Use `pytest` fixtures in `tests/conftest.py` for common setup (like a sample FastAPI app).
- Ensure new features have corresponding tests.
- Follow the TDD approach: write failing tests first, then implement.
