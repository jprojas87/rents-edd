from typing import Iterator, overload


class DoubleLinkedList[T]:
    class Node[NodeT]:
        """Nodo interno de la lista doblemente enlazada."""

        def __init__(
            self,
            item: NodeT,
            prev_node: "DoubleLinkedList.Node[NodeT] | None" = None,
            next_node: "DoubleLinkedList.Node[NodeT] | None" = None,
        ) -> None:
            self.item: NodeT = item
            self.prev: DoubleLinkedList.Node[NodeT] | None = prev_node
            self.next: DoubleLinkedList.Node[NodeT] | None = next_node

    def __init__(self) -> None:
        """Inicializa una lista vacía."""
        self._first: DoubleLinkedList.Node[T] | None = None
        self._last: DoubleLinkedList.Node[T] | None = None
        self._count: int = 0

    def get_last(self) -> T:
        """
        Obtiene el último elemento de la lista.

        Returns:
            El último elemento

        Raises:
            IndexError: Si la lista está vacía
        """
        if self._last is None:
            raise IndexError("get_last from empty list")
        return self._last.item

    def get_first(self) -> T:
        """
        Obtiene el primer elemento de la lista.

        Returns:
            El primer elemento

        Raises:
            IndexError: Si la lista está vacía
        """
        if self._first is None:
            raise IndexError("get_first from empty list")
        return self._first.item

    def add_first(self, item: T, /) -> None:
        """
        Agrega un elemento al inicio de la lista.
        Operación O(1).

        Args:
            item: Elemento a agregar
        """
        new_node = DoubleLinkedList.Node(item)

        if self._first is None:
            self._first = new_node
            self._last = new_node
        else:
            new_node.next = self._first
            self._first.prev = new_node
            self._first = new_node

        self._count += 1

    def add_last(self, item: T, /) -> None:
        """
        Agrega un elemento al final de la lista.
        Operación O(1).

        Args:
            item: Elemento a agregar
        """
        new_node = DoubleLinkedList.Node(item)

        if self._last is None:
            self._first = new_node
        else:
            new_node.prev = self._last
            self._last.next = new_node

        self._last = new_node
        self._count += 1

    def remove(self, item: T, /) -> bool:
        """
        Remueve la primera ocurrencia del elemento especificado.

        Args:
            item: Elemento a remover

        Returns:
            True si se removió el elemento, False si no se encontró
        """
        current = self._first

        while current is not None:
            if current.item == item:
                if current.prev is None:
                    self._first = current.next
                else:
                    current.prev.next = current.next

                if current.next is None:
                    self._last = current.prev
                else:
                    current.next.prev = current.prev

                self._count -= 1
                return True

            current = current.next

        return False

    def pop(self, index: int = -1, /) -> T:
        """
        Remueve y retorna el elemento en la posición especificada.
        Compatible con list.pop() de Python.

        Args:
            index: Índice del elemento (default: -1, último elemento)

        Returns:
            El elemento removido
        """
        if index == -1 or index == self._count - 1:
            return self.remove_last()
        elif index == 0:
            return self.remove_first()

        if index < 0:
            index = self._count + index

        node = self._get_node(index)

        if node.prev is not None:
            node.prev.next = node.next
        if node.next is not None:
            node.next.prev = node.prev

        self._count -= 1
        return node.item

    # === RESTO DE MÉTODOS (sin cambios) ===

    def _get_node(self, index: int, /) -> Node[T]:
        if index < 0 or index >= self._count:
            raise IndexError(f"list index out of range: {index}")

        if index < self._count // 2:
            current = self._first
            for _ in range(index):
                if current is not None:
                    current = current.next
            if current is None:
                raise IndexError(f"list index out of range: {index}")
            return current
        else:
            current = self._last
            for _ in range(self._count - 1 - index):
                if current is not None:
                    current = current.prev
            if current is None:
                raise IndexError(f"list index out of range: {index}")
            return current

    def _validate_index(self, index: int, /, *, allow_append: bool = False) -> None:
        max_index = self._count if allow_append else self._count - 1
        if index < 0 or index > max_index:
            raise IndexError(f"list index out of range: {index}")

    def append(self, item: T, /) -> None:
        self.add_last(item)

    def add(self, item: T, /) -> bool:
        self.add_last(item)
        return True

    def insert(self, index: int, item: T, /) -> None:
        self._validate_index(index, allow_append=True)

        if index == self._count:
            self.add_last(item)
        elif index == 0:
            self.add_first(item)
        else:
            successor = self._get_node(index)
            predecessor = successor.prev

            new_node = DoubleLinkedList.Node(item, predecessor, successor)

            if predecessor is not None:
                predecessor.next = new_node
            successor.prev = new_node

            self._count += 1

    def get(self, index: int, /) -> T:
        return self._get_node(index).item

    def remove_first(self) -> T:
        if self._first is None:
            raise IndexError("remove_first from empty list")

        item = self._first.item
        self._first = self._first.next

        if self._first is None:
            self._last = None
        else:
            self._first.prev = None

        self._count -= 1
        return item

    def remove_last(self) -> T:
        if self._last is None:
            raise IndexError("remove_last from empty list")

        item = self._last.item
        self._last = self._last.prev

        if self._last is None:
            self._first = None
        else:
            self._last.next = None

        self._count -= 1
        return item

    @overload
    def __getitem__(self, index: int, /) -> T: ...

    @overload
    def __getitem__(self, index: slice, /) -> list[T]: ...

    def __getitem__(self, index: int | slice, /) -> T | list[T]:
        if isinstance(index, slice):
            return list(self)[index]

        if index < 0:
            index = self._count + index

        return self.get(index)

    def __setitem__(self, index: int, item: T, /) -> None:
        if index < 0:
            index = self._count + index
        self.set(index, item)

    def clear(self) -> None:
        self._first = None
        self._last = None
        self._count = 0

    def contains(self, item: T, /) -> bool:
        current = self._first
        while current is not None:
            if current.item == item:
                return True
            current = current.next
        return False

    def index(self, item: T, /) -> int:
        current = self._first
        idx = 0
        while current is not None:
            if current.item == item:
                return idx
            current = current.next
            idx += 1
        raise ValueError(f"{item} is not in list")

    def count(self, item: T, /) -> int:
        count = 0
        current = self._first
        while current is not None:
            if current.item == item:
                count += 1
            current = current.next
        return count

    def set(self, index: int, item: T, /) -> T:
        node = self._get_node(index)
        old_item = node.item
        node.item = item
        return old_item

    def reverse(self) -> None:
        current = self._first
        self._first, self._last = self._last, self._first
        while current is not None:
            current.prev, current.next = current.next, current.prev
            current = current.prev

    def is_empty(self) -> bool:
        return self._count == 0

    def size(self) -> int:
        return self._count

    def __iter__(self) -> Iterator[T]:
        current = self._first
        while current is not None:
            yield current.item
            current = current.next

    def __repr__(self) -> str:
        items = list(self)
        return f"DoublyLinkedList({items})"

    def __str__(self) -> str:
        if self.is_empty():
            return "[]"
        items = " <-> ".join(str(item) for item in self)
        return f"[{items}]"