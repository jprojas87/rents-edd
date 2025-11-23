from typing import Iterator


class Stack[T]:
    class Node[E]:
        """Nodo interno de la pila."""

        def __init__(self, item: E, next_node: "Stack.Node[E] | None" = None) -> None:
            self.item: E = item
            self.next: Stack.Node[E] | None = next_node

    def __init__(self) -> None:
        """Inicializa una pila vacía."""
        self._top: Stack.Node[T] | None = None
        self._count: int = 0

    def push(self, item: T, /) -> None:
        """Agrega un elemento en la parte superior de la pila."""
        self._top = Stack.Node(item, self._top)
        self._count += 1

    def pop(self) -> T:
        """
        Remueve y retorna el elemento superior.

        Raises:
            IndexError: Si la pila está vacía
        """
        if self.is_empty() or self._top is None:
            raise IndexError("pop from empty stack")

        item: T = self._top.item
        self._top = self._top.next
        self._count -= 1
        return item

    def peek(self) -> T:
        """
        Retorna el elemento superior sin removerlo.

        Raises:
            IndexError: Si la pila está vacía
        """
        if self.is_empty() or self._top is None:
            raise IndexError("peek from empty stack")
        return self._top.item

    def is_empty(self) -> bool:
        """Indica si la pila está vacía."""
        return self._top is None

    def size(self) -> int:
        """Número de elementos almacenados."""
        return self._count

    def clear(self) -> None:
        """Vacía completamente la pila."""
        self._top = None
        self._count = 0

    def to_list(self) -> list[T]:
        """Convierte la pila en una lista (de arriba hacia abajo)."""
        return list(self)

    def __iter__(self) -> Iterator[T]:
        current = self._top
        while current is not None:
            yield current.item
            current = current.next

    def __contains__(self, item: T, /) -> bool:
        return any(element == item for element in self)

    def __repr__(self) -> str:
        items = list(self)
        return f"Stack({items})"

    def __str__(self) -> str:
        if self.is_empty():
            return "Stack(empty)"
        items = " -> ".join(str(item) for item in self)
        return f"[top: {items}]"
