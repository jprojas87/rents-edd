from typing import List

from datastructures.DoubleLinkedList import DoubleLinkedList


class FavoritesRepository:
    """
    Guarda los ids de propiedades favoritas en una lista doblemente enlazada.
    """

    def __init__(self) -> None:
        self._favorites = DoubleLinkedList()

    def add(self, property_id: int) -> None:
        # Evitar duplicados
        for pid in self._favorites:
            if pid == property_id:
                return
        self._favorites.append(property_id)

    def remove(self, property_id: int) -> bool:
        for pid in self._favorites:
            if pid == property_id:
                self._favorites.remove(pid)
                return True
        return False

    def list_all(self) -> List[int]:
        return [pid for pid in self._favorites]


favorites_repository = FavoritesRepository()
