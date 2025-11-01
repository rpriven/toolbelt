# Python Coding Standards

**Note:** We prefer TypeScript/Bash, but when Python is necessary, follow these standards.

## Type Hints (Required)

Always use type hints for function parameters and return values.

### Function Signatures

```python
from typing import List, Dict, Optional, Tuple

def install_tools(
    tools: Optional[List[str]] = None,
    distro_type: str = 'unknown',
    logger: Optional[logging.Logger] = None
) -> bool:
    """
    Install tools with type-safe parameters

    Args:
        tools: List of package names (None for all)
        distro_type: Distro type for filtering
        logger: Logger instance

    Returns:
        True if successful
    """
    pass
```

### Variable Type Hints

```python
# Simple types
count: int = 0
name: str = "toolbelt"
is_installed: bool = True

# Collections
tools: List[str] = ["nmap", "masscan"]
config: Dict[str, str] = {"key": "value"}
result: Tuple[str, int] = ("success", 200)

# Optional values
logger: Optional[logging.Logger] = None
```

### Common Types

```python
from typing import List, Dict, Set, Tuple, Optional, Union, Any

# Lists
packages: List[str] = []

# Dictionaries
tool_config: Dict[str, Any] = {}

# Optional (can be None)
logger: Optional[logging.Logger] = None

# Union (multiple types)
result: Union[str, int] = "success"

# Tuples with specific types
coordinates: Tuple[int, int] = (10, 20)
```

## Why Type Hints Matter

1. **Catch bugs early** - Type checkers find errors before runtime
2. **Better IDE support** - Autocomplete knows what methods exist
3. **Documentation** - Function signatures show what to pass
4. **Refactoring safety** - Change types, find all affected code

## Type Checking

Run type checker before committing:

```bash
# Install mypy
pip3 install mypy

# Check types
mypy toolbelt.py utils.py config.py installer.py
```

## When to Skip Type Hints

- Quick throwaway scripts (< 50 lines)
- Interactive REPL exploration
- Never skip in production code

## Additional Standards

### Imports

```python
# Standard library first
import os
import sys
from pathlib import Path

# Third party
import requests

# Local modules
from utils import setup_logging
import config
```

### Error Handling

```python
# Specific exceptions, not bare except
try:
    result = risky_operation()
except FileNotFoundError as e:
    logger.error(f"File not found: {e}")
except PermissionError as e:
    logger.error(f"Permission denied: {e}")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
```

### Logging

```python
# Use logging, not print (for production code)
import logging

logger = logging.getLogger(__name__)
logger.info("Operation started")
logger.warning("Potential issue")
logger.error("Operation failed")
```

## Bottom Line

**If we must use Python, we do it right. Type hints are non-negotiable for production code.**
