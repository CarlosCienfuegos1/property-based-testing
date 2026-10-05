from typing import Dict, List, Optional
from src.models import Producto


class RepositorioProducto:
    def __init__(self) -> None:
        self._almacen: Dict[str, Producto] = {}

    def guardar(self, producto: Producto) -> None:
        self._almacen[producto.id] = producto

    def buscar_por_id(self, producto_id: str) -> Optional[Producto]:
        return self._almacen.get(producto_id)

    def buscar_todos(self) -> List[Producto]:
        return list(self._almacen.values())

    def eliminar(self, producto_id: str) -> bool:
        if producto_id in self._almacen:
            del self._almacen[producto_id]
            return True
        return False

    def contar(self) -> int:
        return len(self._almacen)

    def existe(self, producto_id: str) -> bool:
        return producto_id in self._almacen
