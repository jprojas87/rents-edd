from typing import Iterator


class LinkedQueue[T]:
    class Node[E]:
        """Clase interna para representar un nodo de la cola."""

        def __init__(
            self, item: E, next_node: "LinkedQueue.Node[E] | None" = None
        ) -> None:
            self.item: E = item
            self.next: LinkedQueue.Node[E] | None = next_node

    def __init__(self) -> None:
        """Inicializa una cola vacía."""
        self._first: LinkedQueue.Node[T] | None = None
        self._last: LinkedQueue.Node[T] | None = None
        self._count: int = 0

    def enqueue(self, item: T, /) -> None:
        """
        Agrega un elemento al final de la cola.

        Args:
            item: El elemento a agregar
        """
        old_last = self._last
        self._last = LinkedQueue.Node(item, None)

        if self.is_empty():
            self._first = self._last
        else:
            if old_last is not None:
                old_last.next = self._last

        self._count += 1

    def dequeue(self) -> T:
        """
        Remueve y retorna el elemento al frente de la cola.

        Returns:
            El elemento removido

        Raises:
            IndexError: Si la cola está vacía
        """
        if self.is_empty() or self._first is None:
            raise IndexError("dequeue from empty queue")

        item: T = self._first.item
        self._first = self._first.next

        if self.is_empty():
            self._last = None

        self._count -= 1
        return item

    def peek(self) -> T:
        """
        Retorna el elemento al frente sin removerlo.

        Returns:
            El elemento al frente de la cola

        Raises:
            IndexError: Si la cola está vacía
        """
        if self.is_empty() or self._first is None:
            raise IndexError("peek from empty queue")
        return self._first.item

    def is_empty(self) -> bool:
        """Verifica si la cola está vacía."""
        return self._first is None

    def size(self) -> int:
        """Retorna el número de elementos en la cola."""
        return self._count

    def clear(self) -> None:
        """Vacía completamente la cola."""
        self._first = None
        self._last = None
        self._count = 0

    def to_list(self) -> list[T]:
        """Convierte la cola a una lista."""
        return list(self)

    def __iter__(self) -> Iterator[T]:
        """
        Retorna un iterador sobre los elementos de la cola.
        Implementación usando generator (yield).
        """
        current = self._first
        while current is not None:
            yield current.item
            current = current.next

    def __contains__(self, item: T, /) -> bool:
        """
        Verifica si un elemento está en la cola.
        Permite usar: item in queue
        """
        return any(node_item == item for node_item in self)

    def __repr__(self) -> str:
        """Representación en string para debugging."""
        items = list(self)
        return f"LinkedQueue({items})"

    def __str__(self) -> str:
        """Representación en string legible para el usuario."""
        if self.is_empty():
            return "LinkedQueue(empty)"
        items = " <- ".join(str(item) for item in self)
        return f"[front: {items} :back]"