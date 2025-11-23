from typing import List, Optional

from domain.property import Property
from repository.property_repository import property_repository


class PropertyService:
    def create_property(self, title: str, country: str, city: str) -> Property:
        return property_repository.create(title, country, city)

    def get_property(self, property_id: int) -> Optional[Property]:
        return property_repository.get(property_id)

    def update_property(self, property_id: int, title: str, country: str, city: str) -> Optional[Property]:
        return property_repository.update(property_id, title, country, city)

    def delete_property(self, property_id: int) -> bool:
        return property_repository.delete(property_id)

    def list_properties(self) -> List[Property]:
        return property_repository.list_all()


property_service = PropertyService()
