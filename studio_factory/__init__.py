"""Reusable, offline-first creative-production managers.

No model-generation/network calls are implemented in this package.
"""
from .core import Factory, MANAGER_DOMAINS, HANDOFFS, FactoryError

__all__ = ["Factory", "MANAGER_DOMAINS", "HANDOFFS", "FactoryError"]
