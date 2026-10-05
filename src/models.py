import math
from dataclasses import dataclass
from src.exceptions import ErrorValidacion


@dataclass
class Producto:
    id: str
    nombre: str
    precio: float
    stock: int
    categoria: str

    def __post_init__(self) -> None:
        if not isinstance(self.id, str) or not self.id.strip():
            raise ErrorValidacion("El ID debe ser una cadena no vacia")
        if not isinstance(self.nombre, str) or not self.nombre.strip():
            raise ErrorValidacion("El nombre debe ser una cadena no vacia")
        if (
            not isinstance(self.precio, (int, float))
            or isinstance(self.precio, bool)
            or math.isnan(self.precio)
            or math.isinf(self.precio)
            or self.precio <= 0
        ):
            raise ErrorValidacion("El precio debe ser un numero positivo")
        if not isinstance(self.stock, int) or isinstance(self.stock, bool) or self.stock < 0:
            raise ErrorValidacion("El stock debe ser un entero no negativo")
        if not isinstance(self.categoria, str) or not self.categoria.strip():
            raise ErrorValidacion("La categoria debe ser una cadena no vacia")
        self.nombre = self.nombre.strip()
        self.categoria = self.categoria.strip()
        self.precio = float(self.precio)
