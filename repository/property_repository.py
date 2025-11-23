from typing import List, Optional

from datastructures.SymbolTable import SymbolTable  # Ajusta a tu implementación
from domain.property import Property


class PropertyRepository:
    """
    Repositorio de propiedades usando una tabla de símbolos manual (SymbolTable).

    Suposiciones mínimas sobre SymbolTable:
    - put(key, value)
    - get(key) -> value o None
    - remove(key)
    - items() -> iterable de (key, value)
    """

    def __init__(self) -> None:
        self._table = SymbolTable()
        self._next_id = 1

    def create(self, title: str, country: str, city: str) -> Property:
        prop = Property(id=self._next_id, title=title, country=country, city=city)
        self._table.put(self._next_id, prop)
        self._next_id += 1
        return prop

    def get(self, property_id: int) -> Optional[Property]:
        return self._table.get(property_id)

    def update(self, property_id: int, title: str, country: str, city: str) -> Optional[Property]:
        prop = self.get(property_id)
        if prop is None:
            return None
        prop.title = title
        prop.country = country
        prop.city = city
        self._table.put(property_id, prop)
        return prop

    def delete(self, property_id: int) -> bool:
        prop = self.get(property_id)
        if prop is None:
            return False
        self._table.remove(property_id)
        return True

    def list_all(self) -> List[Property]:
        return [value for _, value in self._table.items()]


# Instancia singleton para usar en servicios
property_repository = PropertyRepository()
