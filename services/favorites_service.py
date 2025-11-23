from typing import List

from repository.favorites_repository import favorites_repository
from repository.property_repository import property_repository
from domain.property import Property


class FavoritesService:
    def add_favorite(self, property_id: int) -> None:
        if property_repository.get(property_id) is None:
            raise ValueError("Property not found")
        favorites_repository.add(property_id)

    def remove_favorite(self, property_id: int) -> bool:
        return favorites_repository.remove(property_id)

    def list_favorites(self) -> List[Property]:
        ids = favorites_repository.list_all()
        properties: List[Property] = []
        for pid in ids:
            prop = property_repository.get(pid)
            if prop is not None:
                properties.append(prop)
        return properties


favorites_service = FavoritesService()
