"""
.. include:: ../README.md

## Versioning
We adhere to [Semantic Versioning](https://semver.org/).
You can find the full Changelog [below](#changelog).
"""

from crypticorn.common.logging import configure_logging

configure_logging("crypticorn")

from crypticorn.client import ApiClient

__all__ = ["ApiClient"]
