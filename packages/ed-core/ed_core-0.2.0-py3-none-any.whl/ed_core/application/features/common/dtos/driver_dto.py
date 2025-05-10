from typing import Optional
from uuid import UUID

from ed_domain.core.entities import Driver
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from pydantic import BaseModel

from ed_core.application.features.common.dtos.business_dto import LocationDto
from ed_core.application.features.common.dtos.car_dto import CarDto


class DriverDto(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    profile_image: str
    phone_number: str
    email: Optional[str]
    car: CarDto
    location: LocationDto

    @classmethod
    def from_driver(cls, driver: Driver, uow: ABCUnitOfWork) -> "DriverDto":
        car = uow.car_repository.get(id=driver["car_id"])
        assert car is not None, "Car not found"

        location = uow.location_repository.get(id=driver["location_id"])
        assert location is not None, "Location not found"

        return cls(
            id=driver["id"],
            first_name=driver["first_name"],
            last_name=driver["last_name"],
            profile_image=driver["profile_image"],
            phone_number=driver["phone_number"],
            email=driver.get("email"),
            car=CarDto.from_car(car),
            location=LocationDto.from_location(location),
        )
