from typing import TypeVar, Generic, Optional, List

K = TypeVar('K')
V = TypeVar('V')


class ST(Generic[K, V]):
    """Tabla de símbolos implementada usando una lista de pares clave-valor"""

    def __init__(self) -> None:
        """Crea una tabla de símbolos vacía"""
        self._items: List[tuple[K, V]] = []

    def put(self, key: K, val: Optional[V]) -> None:
        """
        Inserta un par clave-valor en la tabla.
        Elimina la clave de la tabla si el valor es None.

        Args:
            key: La clave a insertar
            val: El valor asociado a la clave (None para eliminar)
        """
        if val is None:
            self.delete(key)
            return


        for i in range(len(self._items)):
            if self._items[i][0] == key:
                # Update existing key
                self._items[i] = (key, val)
                return


        self._items.append((key, val))

    def get(self, key: K) -> Optional[V]:
        """
        Obtiene el valor asociado a la clave.

        Args:
            key: La clave a buscar

        Returns:
            El valor asociado a la clave, o None si la clave no existe
        """
        for k, v in self._items:
            if k == key:
                return v
        return None

    def delete(self, key: K) -> None:
        """
        Elimina la clave (y su valor) de la tabla.

        Args:
            key: La clave a eliminar
        """
        for i in range(len(self._items)):
            if self._items[i][0] == key:
                self._items.pop(i)
                return

    def contains(self, key: K) -> bool:
        """
        Verifica si existe un valor asociado a la clave.

        Args:
            key: La clave a verificar

        Returns:
            True si la clave existe en la tabla, False en caso contrario
        """
        for k, v in self._items:
            if k == key:
                return True
        return False

    def isEmpty(self) -> bool:
        """
        Verifica si la tabla está vacía.

        Returns:
            True si la tabla está vacía, False en caso contrario
        """
        return len(self._items) == 0

    def size(self) -> int:
        """
        Obtiene el número de pares clave-valor en la tabla.

        Returns:
            El número de elementos en la tabla
        """
        return len(self._items)

    def keys(self) -> List[K]:
        """
        Obtiene todas las claves de la tabla.

        Returns:
            Una lista con todas las claves almacenadas
        """
        return [k for k, v in self._items]
