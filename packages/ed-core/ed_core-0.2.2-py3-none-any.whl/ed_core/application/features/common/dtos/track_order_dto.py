from typing import Optional

from ed_domain.core.entities import DeliveryJob, Location
from ed_domain.core.entities.order import Order
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from pydantic import BaseModel

from ed_core.application.features.common.dtos.delivery_job_dto import \
    DeliveryJobDto
from ed_core.application.features.common.dtos.location_dto import LocationDto
from ed_core.application.features.common.dtos.order_dto import OrderDto


class TrackOrderDto(BaseModel):
    order: OrderDto
    delivery_job: Optional[DeliveryJobDto]
    location: Optional[LocationDto]

    @classmethod
    def from_entities(
        cls,
        order: Order,
        uow: ABCUnitOfWork,
        delivery_job: Optional[DeliveryJob] = None,
        location: Optional[Location] = None,
    ) -> "TrackOrderDto":
        return cls(
            order=OrderDto.from_order(order, uow),
            delivery_job=(
                DeliveryJobDto.from_delivery_job(delivery_job, uow)
                if delivery_job
                else None
            ),
            location=LocationDto.from_location(location) if location else None,
        )
