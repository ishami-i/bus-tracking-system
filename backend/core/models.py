from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Route:
    id: int
    name: str
    start_location: str
    end_location: str


@dataclass
class Bus:
    id: int
    route_id: int
    plate_number: str
    capacity: int


@dataclass
class Trip:
    id: int
    bus_id: int
    route_id: int
    started_at: datetime
    finished_at: Optional[datetime] = None


@dataclass
class GPSLog:
    id: int
    bus_id: int
    latitude: float
    longitude: float
    recorded_at: datetime
