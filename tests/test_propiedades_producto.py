from typing import List, Tuple
import pytest
from hypothesis import given, strategies as st
from src.exceptions import ErrorEntidadNoEncontrada, ErrorValidacion
from src.service import ServicioProducto


estrategia_nombre_valido = st.text(
    alphabet=st.characters(blacklist_categories=("Cs", "Cc")),
    min_size=1,
    max_size=50,
).filter(lambda texto: bool(texto.strip()))

estrategia_categoria_valida = st.text(
    alphabet=st.characters(blacklist_categories=("Cs", "Cc")),
    min_size=1,
    max_size=50,
).filter(lambda texto: bool(texto.strip()))

estrategia_precio_valido = st.floats(
    min_value=0.01,
    max_value=1_000_000.0,
    allow_nan=False,
    allow_infinity=False,
)

estrategia_stock_valido = st.integers(min_value=0, max_value=1_000_000)

estrategia_texto_invalido = st.sampled_from(["", " ", "   ", "\t", "\n", " \t \n "])

estrategia_precio_invalido = st.one_of(
    st.floats(max_value=0.0, allow_nan=False, allow_infinity=False),
    st.just(float("nan")),
    st.just(float("inf")),
    st.just(float("-inf")),
)

estrategia_stock_invalido = st.integers(max_value=-1)


# Create
@given(
    nombre=estrategia_nombre_valido,
    precio=estrategia_precio_valido,
    stock=estrategia_stock_valido,
    categoria=estrategia_categoria_valida,
)
def test_crear_valido_persiste(
    nombre: str, precio: float, stock: int, categoria: str
) -> None:
    servicio = ServicioProducto()
    conteo_inicial = servicio.total_productos()

    producto = servicio.crear_producto(nombre, precio, stock, categoria)

    assert servicio.total_productos() == conteo_inicial + 1
    assert isinstance(producto.id, str) and len(producto.id) > 0
    assert producto.nombre == nombre.strip()
    assert producto.precio == float(precio)
    assert producto.stock == stock
    assert producto.categoria == categoria.strip()
    assert servicio.obtener_producto(producto.id) == producto


@given(
    nombre=estrategia_nombre_valido,
    precio_invalido=estrategia_precio_invalido,
    stock=estrategia_stock_valido,
    categoria=estrategia_categoria_valida,
)
def test_crear_precio_invalido_falla(
    nombre: str, precio_invalido: float, stock: int, categoria: str
) -> None:
    servicio = ServicioProducto()
    conteo_inicial = servicio.total_productos()

    with pytest.raises(ErrorValidacion):
        servicio.crear_producto(nombre, precio_invalido, stock, categoria)

    assert servicio.total_productos() == conteo_inicial


@given(
    nombre=estrategia_nombre_valido,
    precio=estrategia_precio_valido,
    stock_invalido=estrategia_stock_invalido,
    categoria=estrategia_categoria_valida,
)
def test_crear_stock_invalido_falla(
    nombre: str, precio: float, stock_invalido: int, categoria: str
) -> None:
    servicio = ServicioProducto()
    conteo_inicial = servicio.total_productos()

    with pytest.raises(ErrorValidacion):
        servicio.crear_producto(nombre, precio, stock_invalido, categoria)

    assert servicio.total_productos() == conteo_inicial


@given(
    nombre_invalido=estrategia_texto_invalido,
    precio=estrategia_precio_valido,
    stock=estrategia_stock_valido,
    categoria=estrategia_categoria_valida,
)
def test_crear_nombre_vacio_falla(
    nombre_invalido: str, precio: float, stock: int, categoria: str
) -> None:
    servicio = ServicioProducto()
    conteo_inicial = servicio.total_productos()

    with pytest.raises(ErrorValidacion):
        servicio.crear_producto(nombre_invalido, precio, stock, categoria)

    assert servicio.total_productos() == conteo_inicial


# Read
@given(
    datos_productos=st.lists(
        st.tuples(
            estrategia_nombre_valido,
            estrategia_precio_valido,
            estrategia_stock_valido,
            estrategia_categoria_valida,
        ),
        min_size=1,
        max_size=15,
    )
)
def test_obtener_por_id_es_idempotente(
    datos_productos: List[Tuple[str, float, int, str]]
) -> None:
    servicio = ServicioProducto()
    productos_creados = [
        servicio.crear_producto(nombre, precio, stock, categoria)
        for nombre, precio, stock, categoria in datos_productos
    ]

    for producto in productos_creados:
        primera_consulta = servicio.obtener_producto(producto.id)
        segunda_consulta = servicio.obtener_producto(producto.id)
        assert primera_consulta == producto
        assert segunda_consulta == producto
        assert primera_consulta == segunda_consulta


@given(id_inexistente=st.uuids().map(str))
def test_obtener_id_inexistente_falla(id_inexistente: str) -> None:
    servicio = ServicioProducto()
    with pytest.raises(ErrorEntidadNoEncontrada):
        servicio.obtener_producto(id_inexistente)


@given(
    datos_productos=st.lists(
        st.tuples(
            estrategia_nombre_valido,
            estrategia_precio_valido,
            estrategia_stock_valido,
            estrategia_categoria_valida,
        ),
        min_size=0,
        max_size=10,
    )
)
def test_listar_retorna_todos(
    datos_productos: List[Tuple[str, float, int, str]]
) -> None:
    servicio = ServicioProducto()
    productos_creados = [
        servicio.crear_producto(nombre, precio, stock, categoria)
        for nombre, precio, stock, categoria in datos_productos
    ]

    listados = servicio.listar_productos()
    assert len(listados) == len(productos_creados)
    assert {p.id for p in listados} == {p.id for p in productos_creados}
    assert all(p in productos_creados for p in listados)



# Update
@given(
    nombre_inicial=estrategia_nombre_valido,
    precio_inicial=estrategia_precio_valido,
    stock_inicial=estrategia_stock_valido,
    categoria_inicial=estrategia_categoria_valida,
    nuevo_nombre=estrategia_nombre_valido,
    nuevo_precio=estrategia_precio_valido,
)
def test_actualizar_modifica_solo_indicados(
    nombre_inicial: str,
    precio_inicial: float,
    stock_inicial: int,
    categoria_inicial: str,
    nuevo_nombre: str,
    nuevo_precio: float,
) -> None:
    servicio = ServicioProducto()
    producto = servicio.crear_producto(
        nombre_inicial, precio_inicial, stock_inicial, categoria_inicial
    )

    actualizado = servicio.actualizar_producto(
        producto.id, nombre=nuevo_nombre, precio=nuevo_precio
    )

    assert actualizado.id == producto.id
    assert actualizado.nombre == nuevo_nombre.strip()
    assert actualizado.precio == float(nuevo_precio)
    assert actualizado.stock == stock_inicial
    assert actualizado.categoria == categoria_inicial.strip()
    assert servicio.obtener_producto(producto.id) == actualizado
    assert servicio.total_productos() == 1


@given(
    nombre=estrategia_nombre_valido,
    precio=estrategia_precio_valido,
    stock=estrategia_stock_valido,
    categoria=estrategia_categoria_valida,
    precio_invalido=estrategia_precio_invalido,
)
def test_actualizar_precio_invalido_falla(
    nombre: str,
    precio: float,
    stock: int,
    categoria: str,
    precio_invalido: float,
) -> None:
    servicio = ServicioProducto()
    producto = servicio.crear_producto(nombre, precio, stock, categoria)

    with pytest.raises(ErrorValidacion):
        servicio.actualizar_producto(producto.id, precio=precio_invalido)

    guardado = servicio.obtener_producto(producto.id)
    assert guardado == producto


@given(
    id_inexistente=st.uuids().map(str),
    nuevo_nombre=estrategia_nombre_valido,
)
def test_actualizar_id_inexistente_falla(
    id_inexistente: str, nuevo_nombre: str
) -> None:
    servicio = ServicioProducto()
    with pytest.raises(ErrorEntidadNoEncontrada):
        servicio.actualizar_producto(id_inexistente, nombre=nuevo_nombre)


# Delete
@given(
    datos_productos=st.lists(
        st.tuples(
            estrategia_nombre_valido,
            estrategia_precio_valido,
            estrategia_stock_valido,
            estrategia_categoria_valida,
        ),
        min_size=1,
        max_size=8,
    ),
    indice_eliminar=st.integers(min_value=0, max_value=7),
)
def test_eliminar_decrementa_y_remueve(
    datos_productos: List[Tuple[str, float, int, str]],
    indice_eliminar: int,
) -> None:
    servicio = ServicioProducto()
    creados = [
        servicio.crear_producto(nombre, precio, stock, categoria)
        for nombre, precio, stock, categoria in datos_productos
    ]

    objetivo = creados[indice_eliminar % len(creados)]
    conteo_inicial = servicio.total_productos()

    resultado_eliminacion = servicio.eliminar_producto(objetivo.id)

    assert resultado_eliminacion is True
    assert servicio.total_productos() == conteo_inicial - 1
    assert objetivo.id not in {p.id for p in servicio.listar_productos()}

    with pytest.raises(ErrorEntidadNoEncontrada):
        servicio.obtener_producto(objetivo.id)

    ids_restantes = {p.id for p in creados if p.id != objetivo.id}
    assert {p.id for p in servicio.listar_productos()} == ids_restantes


@given(id_inexistente=st.uuids().map(str))
def test_eliminar_id_inexistente_falla(
    id_inexistente: str,
) -> None:
    servicio = ServicioProducto()
    with pytest.raises(ErrorEntidadNoEncontrada):
        servicio.eliminar_producto(id_inexistente)


@given(
    nombre=estrategia_nombre_valido,
    precio=estrategia_precio_valido,
    stock=estrategia_stock_valido,
    categoria=estrategia_categoria_valida,
)
def test_eliminar_duplicado_falla(
    nombre: str, precio: float, stock: int, categoria: str
) -> None:
    servicio = ServicioProducto()
    producto = servicio.crear_producto(nombre, precio, stock, categoria)

    assert servicio.eliminar_producto(producto.id) is True

    with pytest.raises(ErrorEntidadNoEncontrada):
        servicio.eliminar_producto(producto.id)
