
For backend development, use `uv` for dependency management.

Useful Commands

    # Sync dependencies from lockfile
    uv sync

    # Add a new package
    uv add <PACKAGE-NAME>

    # Run Python files
    uv run python <PYTHON-FILE>

    # Initialize the database (SQLite/Postgres)
    uv run python init_db.py

    # Run integration tests (SQLite)
    uv run pytest tests_integration/