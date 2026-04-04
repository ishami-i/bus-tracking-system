"""Core domain layer for the bus tracking system.

This package contains pure Python models and business logic that are
independent from any web framework.
"""

from .models import Bus, Route, Trip, GPSLog  # noqa: F401
