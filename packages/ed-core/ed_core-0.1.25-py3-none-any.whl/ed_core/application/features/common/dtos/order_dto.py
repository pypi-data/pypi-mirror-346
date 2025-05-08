from datetime import datetime
from typing import Optional
from uuid import UUID

from ed_domain.core.entities.order import Order, OrderStatus, Parcel
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from pydantic import BaseModel

from ed_core.application.features.common.dtos.consumer_dto import ConsumerDto


class OrderDto(BaseModel):
    id: UUID
    consumer: ConsumerDto
    latest_time_of_delivery: datetime
    parcel: Parcel
    order_status: OrderStatus
    delivery_job_id: Optional[UUID]

    @classmethod
    def from_order(
        cls,
        order: Order,
        uow: ABCUnitOfWork,
    ) -> "OrderDto":
        assert order["consumer_id"] is not None, "Consumer ID cannot be None"
        order_consumer = uow.consumer_repository.get(id=order["consumer_id"])
        assert order_consumer is not None, "Consumer not found"
        return cls(
            id=order["id"],
            consumer=ConsumerDto.from_consumer(order_consumer),
            latest_time_of_delivery=order["latest_time_of_delivery"],
            parcel=order["parcel"],
            order_status=order["order_status"],
            delivery_job_id=order.get("delivery_job_id"),
        )
