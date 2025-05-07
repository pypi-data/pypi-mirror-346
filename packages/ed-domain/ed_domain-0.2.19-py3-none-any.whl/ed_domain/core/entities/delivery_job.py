from datetime import datetime
from enum import StrEnum
from typing import NotRequired, TypedDict
from uuid import UUID

from ed_domain.core.entities.base_entity import BaseEntity


class WayPointType(StrEnum):
    PICKUP = "PICKUP"
    DROP_OFF = "DROP_OFF"


class WayPoint(TypedDict):
    order_id: UUID
    type: WayPointType
    eta: datetime
    sequence: int


class DeliveryJobStatus(StrEnum):
    AVAILABLE = "available"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class DeliveryJob(BaseEntity):
    waypoints: list[WayPoint]
    status: DeliveryJobStatus
    estimated_payment: float
    estimated_completion_time: datetime
    estimated_distance_in_kms: float
    estimated_time_in_minutes: int
    driver_id: NotRequired[UUID]
    driver_payment_id: NotRequired[UUID]
