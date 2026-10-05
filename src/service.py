import uuid
from typing import List, Optional
from src.exceptions import ErrorEntidadNoEncontrada
from src.models import Producto
from src.repository import RepositorioProducto


class ServicioProducto:
    def __init__(self, repositorio: Optional[RepositorioProducto] = None) -> None:
        self.repositorio = repositorio if repositorio is not None else RepositorioProducto()

    # Create
    def crear_producto(self, nombre: str, precio: float, stock: int, categoria: str) -> Producto:
        producto_id = str(uuid.uuid4())
        producto = Producto(
            id=producto_id,
            nombre=nombre,
            precio=precio,
            stock=stock,
            categoria=categoria,
        )
        self.repositorio.guardar(producto)
        return producto

    # Read
    def obtener_producto(self, producto_id: str) -> Producto:
        producto = self.repositorio.buscar_por_id(producto_id)
        if producto is None:
            raise ErrorEntidadNoEncontrada(f"Producto con id {producto_id} no encontrado")
        return producto

    def listar_productos(self) -> List[Producto]:
        return self.repositorio.buscar_todos()

    # Update
    def actualizar_producto(
        self,
        producto_id: str,
        nombre: Optional[str] = None,
        precio: Optional[float] = None,
        stock: Optional[int] = None,
        categoria: Optional[str] = None,
    ) -> Producto:
        existente = self.obtener_producto(producto_id)
        producto_actualizado = Producto(
            id=producto_id,
            nombre=nombre if nombre is not None else existente.nombre,
            precio=precio if precio is not None else existente.precio,
            stock=stock if stock is not None else existente.stock,
            categoria=categoria if categoria is not None else existente.categoria,
        )
        self.repositorio.guardar(producto_actualizado)
        return producto_actualizado

    # Delete
    def eliminar_producto(self, producto_id: str) -> bool:
        if not self.repositorio.existe(producto_id):
            raise ErrorEntidadNoEncontrada(f"Producto con id {producto_id} no encontrado")
        return self.repositorio.eliminar(producto_id)

    def total_productos(self) -> int:
        return self.repositorio.contar()
