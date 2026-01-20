# Tests directory

This directory contains automated tests for the OnTrack application.

## Test Structure

- `conftest.py` - Pytest configuration and shared fixtures
- `test_models.py` - Tests for SQLModel database models
- `test_database.py` - Tests for database access functions

## Running Tests

### Run all tests
```bash
uv run pytest
```

### Run with coverage report
```bash
uv run pytest --cov=. --cov-report=html --cov-report=term
```

### Run specific test file
```bash
uv run pytest tests/test_models.py
```

### Run specific test class
```bash
uv run pytest tests/test_models.py::TestSkaterModel
```

### Run specific test
```bash
uv run pytest tests/test_models.py::TestSkaterModel::test_create_basic_skater
```

### Run with verbose output
```bash
uv run pytest -v
```

## Test Coverage

The test suite covers:

### Models (`test_models.py`)
- ✅ Skater model creation and defaults
- ✅ Guardian information fields
- ✅ Coach tagging
- ✅ Practice model with all fields
- ✅ Attendance model with relationships
- ✅ Model defaults and validation

### Database Functions (`test_database.py`)
- ✅ Skater CRUD operations
- ✅ Practice CRUD operations
- ✅ Attendance tracking
- ✅ Soft delete for skaters
- ✅ Hard delete for practices
- ✅ Cascade deletes
- ✅ Attendance statistics calculation
- ✅ Active/inactive filtering
- ✅ Ordering and limits

## Fixtures

### `session`
Provides a fresh in-memory SQLite database for each test. This ensures:
- Tests are isolated from each other
- No test data pollution
- Fast test execution
- No need to clean up after tests

## Writing New Tests

When adding new features, add corresponding tests:

1. **Model changes**: Add tests to `test_models.py`
2. **Database functions**: Add tests to `test_database.py`
3. **New modules**: Create new test files following the `test_*.py` pattern

### Example Test

```python
def test_my_feature(session):
    """Test description."""
    # Arrange
    skater = create_skater(session, name="Test")

    # Act
    result = my_function(session, skater.id)

    # Assert
    assert result is not None
```

## Continuous Integration

Tests run automatically:
- On every commit (via pre-commit hooks)
- On pull requests (via GitHub Actions)
- Before deployment

## Coverage Goals

- Aim for >80% code coverage
- All critical paths must be tested
- Edge cases should be covered
