from typing import List, Optional

from datastructures.SymbolTable import ST
from domain.property import Property


class PropertyRepository:
    """
    Repositorio de propiedades usando una tabla de símbolos manual (ST).

    Suposiciones mínimas sobre ST:
    - put(key, value)
    - get(key) -> value o None
    - delete(key)
    - keys() -> lista de claves almacenadas
    """

    def __init__(self) -> None:
        self._table = ST()
        self._next_id = 1

    def create(self, address: str, body: str, rating: int) -> Property:
        prop = Property(id=self._next_id, address=address, body=body, rating=rating)
        self._table.put(self._next_id, prop)
        self._next_id += 1
        return prop

    def get(self, property_id: int) -> Optional[Property]:
        return self._table.get(property_id)

    def update(self, property_id: int, address: str, body: str, rating: int) -> Optional[Property]:
        prop = self.get(property_id)
        if prop is None:
            return None
        prop.address = address
        prop.body = body
        prop.rating = rating
        self._table.put(property_id, prop)
        return prop

    def delete(self, property_id: int) -> bool:
        prop = self.get(property_id)
        if prop is None:
            return False
        self._table.delete(property_id)
        return True

    def list_all(self) -> List[Property]:
        properties: List[Property] = []
        for key in self._table.keys():
            prop = self._table.get(key)
            if prop is not None:
                properties.append(prop)
        return properties


# Instancia singleton para usar en servicios
property_repository = PropertyRepository()
