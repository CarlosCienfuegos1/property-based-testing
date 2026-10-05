# Sistema de Gestión de Productos con Property-Based Testing

## 1. Descripción del Dominio

La entidad principal es `Producto`, la cual define las siguientes invariantes y reglas de negocio:

- `id`: Identificador único (UUID en formato cadena de texto).
- `nombre`: Cadena de texto no vacía (no admite solo espacios en blanco).
- `precio`: Número finito estrictamente positivo (`precio > 0`).
- `stock`: Entero mayor o igual a cero (`stock >= 0`).
- `categoria`: Cadena de texto no vacía (no admite solo espacios en blanco).

---

## 2. Operaciones del Sistema (CRUD)

La lógica de negocio se encuentra en `ServicioProducto` y se apoya en un `RepositorioProducto` en memoria:

- **Create**: `crear_producto(nombre, precio, stock, categoria)`
- **Read**: `obtener_producto(producto_id)` y `listar_productos()`
- **Update**: `actualizar_producto(producto_id, nombre, precio, stock, categoria)`
- **Delete**: `eliminar_producto(producto_id)`

---

## 3. Propiedades Validadas (Invariantes del Sistema)

### Create
- **`test_crear_valido_persiste`**: Para cualquier conjunto de atributos válidos generados, la creación asigna un ID único, incrementa el total de entidades en 1 y persiste exactamente los datos suministrados.
- **`test_crear_precio_invalido_falla`**: Un precio menor o igual a cero, o valores especiales (NaN, infinito), rechazan la creación con `ErrorValidacion` y no modifican el estado.
- **`test_crear_stock_invalido_falla`**: Un stock negativo siempre rechaza la creación con `ErrorValidacion` y no altera el contador de productos.
- **`test_crear_nombre_vacio_falla`**: Nombres vacíos o con solo espacios en blanco rechazan la creación y preservan el estado del sistema.

### Read
- **`test_obtener_por_id_es_idempotente`**: Para cualquier producto persistido, la consulta por ID es idempotente (múltiples lecturas retornan el mismo objeto sin alterar el estado).
- **`test_obtener_id_inexistente_falla`**: Para cualquier ID generado que no exista en el sistema, la consulta lanza siempre `ErrorEntidadNoEncontrada`.
- **`test_listar_retorna_todos`**: Para cualquier cantidad de productos creados, el listado general contiene exactamente todas y únicamente las entidades activas.

### Update
- **`test_actualizar_modifica_solo_indicados`**: Al actualizar un subconjunto de campos, se aplican los nuevos valores y se preservan el ID y los atributos no modificados.
- **`test_actualizar_precio_invalido_falla`**: Intentar actualizar un producto con un precio inválido falla con `ErrorValidacion` y mantiene el producto almacenado sin alteraciones.
- **`test_actualizar_id_inexistente_falla`**: Intentar actualizar un ID que no existe en el sistema lanza `ErrorEntidadNoEncontrada`.

### Delete
- **`test_eliminar_decrementa_y_remueve`**: Eliminar un producto existente decrementa el total en 1, lo remueve del listado general y hace que consultas posteriores por su ID fallen con `ErrorEntidadNoEncontrada`.
- **`test_eliminar_id_inexistente_falla`**: Intentar eliminar un ID inexistente lanza `ErrorEntidadNoEncontrada`.
- **`test_eliminar_duplicado_falla`**: La eliminación no es doblemente aplicable; la segunda llamada sobre el mismo ID falla con `ErrorEntidadNoEncontrada`.

---

## 4. Estructura del Proyecto

```text
.
├── src/
│   ├── __init__.py
│   ├── exceptions.py             # ErrorDominio, ErrorValidacion, ErrorEntidadNoEncontrada
│   ├── models.py                 # Entidad Producto con validaciones invariantes
│   ├── repository.py             # RepositorioProducto en memoria
│   └── service.py                # ServicioProducto con operaciones CRUD
├── tests/
│   ├── __init__.py
│   └── test_propiedades_producto.py  # Pruebas de propiedades agrupadas por Create, Read, Update, Delete
├── .gitignore
├── README.md
└── requirements.txt              # hypothesis y pytest
```

---

## 5. Instalación y Ejecución

### Requisitos previos

- Python 3.10 o superior
- `pip`

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

### Ejecución de las pruebas

Para ejecutar toda la suite de pruebas basadas en propiedades:

```bash
pytest -v
```

Para ver estadísticas de Hypothesis:

```bash
pytest -v --hypothesis-show-statistics
```
