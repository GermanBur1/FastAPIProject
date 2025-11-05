# Documentación del Proyecto de Árbol Binario para Ventas de Vehículos

## Estructura del Proyecto

### 1. Modelos (`app/models/`)

#### `schemas.py`
Define los modelos de datos usando Pydantic para validación y documentación de la API:

- **`Color` (Enumeración)**: Define los colores disponibles para los vehículos.
  
- **`CarSaleBase`**: Modelo base para las ventas de vehículos.
  - `license_plate`: Placa del vehículo (6-10 caracteres)
  - `brand`: Marca del vehículo (2-50 caracteres)
  - `color`: Color del vehículo (usando la enumeración Color)
  - `price`: Precio del vehículo (mayor a 0)
  - `sale_date`: Fecha de la venta (se genera automáticamente)

- **`CarSaleCreate`**: Modelo para la creación de nuevas ventas (hereda de CarSaleBase).

- **`CarSaleUpdate`**: Modelo para actualizar ventas existentes (todos los campos son opcionales).

- **`CarSale`**: Modelo completo que incluye un ID único.

- **`TreeStats`**: Modelo para las estadísticas del árbol.

#### `binary_tree.py`
Implementa la lógica del árbol binario de búsqueda:

- **Clase `TreeNode`**:
  - `__init__(self, data: CarSale)`: Inicializa un nodo con datos.

- **Clase `BinarySearchTree`**:
  - `__init__(self)`: Inicializa el árbol vacío.
  - `_ensure_csv_headers(self)`: Crea el archivo CSV con las cabeceras si no existe.
  - `_load_from_csv(self)`: Carga datos desde el archivo CSV al árbol.
  - `_save_to_csv(self, node)`: Guarda los datos del árbol en CSV (recursivo).
  - `save_tree(self)`: Guarda todo el árbol en el archivo CSV.
  - `insert(self, data)`: Inserta un nuevo nodo en el árbol.
  - `find(self, license_plate)`: Busca un nodo por placa.
  - `_find_min(self, node)`: Encuentra el nodo mínimo en un subárbol.
  - `delete(self, license_plate)`: Elimina un nodo por placa.
  - `update(self, license_plate, update_data)`: Actualiza los datos de un nodo.
  - `in_order_traversal(self)`: Recorrido inorden (izquierda, raíz, derecha).
  - `pre_order_traversal(self)`: Recorrido preorden (raíz, izquierda, derecha).
  - `post_order_traversal(self)`: Recorrido postorden (izquierda, derecha, raíz).
  - `get_tree_stats(self)`: Obtiene estadísticas del árbol.
  - `find_path(self, start_plate, end_plate)`: Encuentra el camino entre dos nodos.
  - `find_longest_path(self)`: Encuentra el camino más largo en el árbol.

### 2. Controladores (`app/controllers/`)

#### `car_sales_controller.py`
Maneja la lógica de negocio:

- **`CarSalesController`**:
  - `create_car_sale(car_sale)`: Crea una nueva venta de vehículo.
  - `get_car_sale(license_plate)`: Obtiene una venta por placa.
  - `update_car_sale(license_plate, update_data)`: Actualiza una venta existente.
  - `delete_car_sale(license_plate)`: Elimina una venta.
  - `get_tree_traversal(order)`: Obtiene un recorrido del árbol.
  - `get_tree_statistics()`: Obtiene estadísticas del árbol.
  - `get_path_between_nodes(start_plate, end_plate)`: Obtiene el camino entre dos nodos.
  - `get_longest_path()`: Obtiene el camino más largo en el árbol.

### 3. Rutas (`app/routers/`)

#### `car_sales.py`
Define los endpoints de la API:

- **Endpoints**:
  - `POST /api/car-sales/`: Crea una nueva venta.
  - `GET /api/car-sales/{license_plate}`: Obtiene una venta por placa.
  - `PUT /api/car-sales/{license_plate}`: Actualiza una venta.
  - `DELETE /api/car-sales/{license_plate}`: Elimina una venta.
  - `GET /api/car-sales/traversal/{order}`: Obtiene un recorrido del árbol.
  - `GET /api/car-sales/stats/`: Obtiene estadísticas del árbol.
  - `GET /api/car-sales/path/{start_plate}/{end_plate}`: Obtiene el camino entre dos nodos.
  - `GET /api/car-sales/longest-path/`: Obtiene el camino más largo.

### 4. Punto de Entrada Principal (`main.py`)

Configura la aplicación FastAPI:

- Configuración de CORS para permitir peticiones desde cualquier origen.
- Inclusión del enrutador de ventas de vehículos.
- Documentación automática con Swagger UI y ReDoc.

## Flujo de Datos

1. **Creación de una Venta**:
   - El cliente envía una solicitud POST a `/api/car-sales/` con los datos del vehículo.
   - El enrutador valida los datos con Pydantic.
   - El controlador crea un nuevo nodo en el árbol.
   - El árbol guarda automáticamente los cambios en el archivo CSV.

2. **Búsqueda de una Venta**:
   - El cliente solicita una venta por placa.
   - El árbol realiza una búsqueda binaria.
   - Se devuelve el vehículo si se encuentra.

3. **Eliminación de una Venta**:
   - El cliente solicita eliminar una venta por placa.
   - El árbol elimina el nodo correspondiente.
   - Se actualiza el archivo CSV.

4. **Recorridos del Árbol**:
   - El cliente solicita un recorrido específico.
   - El árbol realiza el recorrido solicitado.
   - Se devuelve la lista de vehículos en el orden correspondiente.

5. **Estadísticas del Árbol**:
   - El cliente solicita estadísticas.
   - El árbol calcula altura, número de nodos, hojas y nodos por nivel.
   - Se devuelven las estadísticas.

## Consideraciones de Diseño

- **Persistencia**: Los datos se guardan automáticamente en un archivo CSV.
- **Validación**: Se usa Pydantic para validar los datos de entrada.
- **Documentación**: La API está documentada automáticamente con Swagger UI y ReDoc.
- **Manejo de Errores**: Se devuelven códigos de estado HTTP apropiados.

## Uso de la API

La API está diseñada para ser utilizada desde cualquier cliente HTTP. La documentación interactiva está disponible en:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Requisitos

- Python 3.7+
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clonar el repositorio
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar la aplicación:
   ```bash
   uvicorn main:app --reload
   ```

## Ejemplo de Uso con cURL

```bash
# Crear una nueva venta
curl -X 'POST' \
  'http://localhost:8000/api/car-sales/' \
  -H 'Content-Type: application/json' \
  -d '{
    "license_plate": "ABC123",
    "brand": "Toyota",
    "color": "blue",
    "price": 25000.0
  }'

# Obtener una venta por placa
curl -X 'GET' 'http://localhost:8000/api/car-sales/ABC123'

# Obtener estadísticas del árbol
curl -X 'GET' 'http://localhost:8000/api/car-sales/stats/'

# Obtener el recorrido inorden
curl -X 'GET' 'http://localhost:8000/api/car-sales/traversal/inorder'

# Encontrar el camino más largo
curl -X 'GET' 'http://localhost:8000/api/car-sales/longest-path/'
```

## Estructura del Proyecto

```
FastAPIProject/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── schemas.py
│   │   └── binary_tree.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── car_sales_controller.py
│   └── routers/
│       ├── __init__.py
│       └── car_sales.py
├── main.py
├── requirements.txt
└── car_sales.csv (se crea automáticamente)
```
