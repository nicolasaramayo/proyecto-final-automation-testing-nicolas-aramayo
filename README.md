# Proyecto Final - Automatizacion QA

Framework de automatizacion de pruebas que combina pruebas de UI con Selenium WebDriver y pruebas de API con la biblioteca Requests, utilizando Python, Pytest y el patron Page Object Model.

---

## Proposito del Proyecto

Este proyecto implementa una suite de pruebas automatizadas de extremo a extremo (E2E) sobre el sitio web de demostracion [SauceDemo](https://www.saucedemo.com), complementada con pruebas de API contra [ReqRes](https://reqres.in/).

El framework demuestra la aplicacion de patrones de disenio, buenas practicas de automatizacion y generacion de reportes para facilitar la interpretacion de resultados.

---

## Tecnologias Utilizadas

| Tecnologia | Version | Proposito |
|---|---|---|
| Python | 3.8+ | Lenguaje de programacion principal |
| Pytest | 8.2.0 | Framework de ejecucion de pruebas |
| Selenium WebDriver | 4.21.0 | Automatizacion de interfaces web |
| pytest-html | 4.1.1 | Generacion de reportes HTML |
| WebDriver Manager | 4.0.1 | Gestion automatica de ChromeDriver |
| Requests | 2.31.0 | Pruebas de API REST |
| Google Chrome | Ultima version | Navegador utilizado para las pruebas |

---

## Estructura del Proyecto

```
Entrega-Final-QA/
|
|-- conftest.py                  # Fixtures globales y hooks de Pytest
|-- pytest.ini                   # Configuracion de Pytest
|-- requirements.txt             # Dependencias del proyecto
|-- .gitignore                   # Archivos ignorados por Git
|-- README.md                    # Este archivo
|
|-- pages/                       # Page Objects (patron POM)
|   |-- __init__.py
|   |-- base_page.py             # Clase base con metodos comunes de interaccion
|   |-- login_page.py            # Page Object de la pagina de login
|   |-- inventory_page.py        # Page Object de la pagina de inventario
|   |-- cart_page.py             # Page Object del carrito de compras
|   +-- checkout_page.py         # Page Object del proceso de checkout
|
|-- tests/                       # Modulos de prueba
|   |-- __init__.py
|   |-- test_ui_saucedemo.py     # Pruebas de UI (5 casos)
|   +-- test_api_reqres.py       # Pruebas de API (4 casos)
|
|-- utils/                       # Modulos de utilidad
|   |-- __init__.py
|   |-- config.py                # Constantes, URLs, credenciales y localizadores
|   +-- helpers.py               # Funciones helper reutilizables
|
|-- datos/                       # Datos de prueba
|   +-- users.json               # Credenciales para pruebas parametrizadas

|-- logs/                        # Archivos de log generados en ejecucion
|   +-- .gitkeep

|-- reports/                     # Reportes generados
|   |-- .gitkeep
|   |-- reporte.html             # Reporte HTML (generado por pytest-html)
|   +-- screenshots/             # Capturas de pantalla ante fallos
|       +-- .gitkeep
|
+-- .github/
    +-- workflows/
        +-- pytest.yml           # Pipeline de GitHub Actions
```

---

## Instalacion y Configuracion

### Prerequisitos

- Python 3.8 o superior
- Google Chrome (version actualizada)
- Git

Verificar instalacion de Python:

```bash
python --version
```

### 1. Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd Entrega-Final-QA
```

### 2. Crear y Activar el Entorno Virtual

```bash
# Crear el entorno virtual
python -m venv venv

# Activar en Windows (PowerShell)
venv\Scripts\activate

# Activar en Windows (CMD)
venv\Scripts\activate.bat

# Activar en macOS/Linux
source venv/bin/activate
```

Cuando el entorno esta activo, se vera `(venv)` al inicio del prompt.

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

WebDriver Manager descargara automaticamente el ChromeDriver compatible con la version de Chrome instalada. No es necesario descargarlo manualmente.

---

## Ejecucion de Pruebas

### Ejecutar todos los tests

```bash
pytest
```

El reporte se genera automaticamente en `reports/reporte.html` segun la configuracion en `pytest.ini`.

### Ejecutar con reporte HTML especificando la ruta

```bash
pytest -v --html=reports/reporte.html --self-contained-html
```

### Ejecutar un modulo de prueba especifico

```bash
# Solo pruebas de UI
pytest tests/test_ui_saucedemo.py -v

# Solo pruebas de API
pytest tests/test_api_reqres.py -v
```

### Ejecutar un test individual

```bash
pytest tests/test_ui_saucedemo.py::test_successful_login -v
```

### Ver logs en consola durante la ejecucion

```bash
pytest -v -s --log-cli-level=INFO
```

---

## Casos de Prueba

### Pruebas de UI (Selenium WebDriver)

| # | Test | Descripcion |
|---|------|-------------|
| 1 | `test_successful_login` | Verifica que un usuario valido puede iniciar sesion y es redirigido al inventario |
| 2 | `test_failed_login` | Verifica que credenciales incorrectas muestran mensaje de error (parametrizado con 3 casos) |
| 3 | `test_catalog_elements_and_count` | Verifica visibilidad de elementos del catalogo y cantidad exacta de productos |
| 4 | `test_add_to_cart_updates_badge` | Verifica que agregar un producto incrementa el badge del carrito |
| 5 | `test_complete_checkout_flow` | Flujo completo: login, catalogo, carrito, checkout y confirmacion |

### Pruebas de API (Requests)

| # | Test | Metodo | Descripcion |
|---|------|--------|-------------|
| 1 | `test_get_user` | GET | Obtiene detalles de un usuario y valida estructura de respuesta |
| 2 | `test_create_user` | POST | Crea un usuario y valida codigo 201 y campos de respuesta |
| 3 | `test_delete_user` | DELETE | Elimina un usuario y valida codigo 204 |
| 4 | `test_user_creation_and_update_chain` | POST + PUT | Encadenamiento de peticiones: crear y luego actualizar |

### Metodos HTTP Utilizados

| Metodo | Proposito | Codigo Esperado | Ejemplo |
|--------|-----------|-----------------|---------|
| **GET** | Obtener datos de un recurso existente | 200 (OK) | `GET /api/users/2` retorna los datos del usuario con ID 2 |
| **POST** | Crear un nuevo recurso en el servidor | 201 (Created) | `POST /api/users` con body `{"name": "morpheus", "job": "leader"}` crea un usuario |
| **PUT** | Actualizar un recurso existente completo | 200 (OK) | `PUT /api/users/2` con body `{"name": "neo", "job": "saviour"}` actualiza el usuario |
| **DELETE** | Eliminar un recurso del servidor | 204 (No Content) | `DELETE /api/users/2` elimina el usuario con ID 2 |

Cada test valida tanto el codigo de estado HTTP como la estructura del JSON de respuesta, asegurando que la API se comporta correctamente ante diferentes operaciones CRUD (Create, Read, Update, Delete).

---

## Reportes

### Reporte HTML

Al ejecutar `pytest`, se genera automaticamente el archivo `reports/reporte.html`.

Para visualizarlo:

```bash
# Windows
start reports\reporte.html

# macOS
open reports/reporte.html
```

El reporte incluye:

- Resumen de tests ejecutados, pasados, fallidos y omitidos
- Detalle de cada test con duracion, logs y mensajes de error
- Referencias a capturas de pantalla en caso de fallos

### Capturas de Pantalla ante Fallos

Cuando un test falla, el hook `pytest_runtest_makereport` en `conftest.py` captura automaticamente una screenshot del estado del navegador en el momento del fallo.

Las imagenes se guardan en:

```
reports/screenshots/{nombre_del_test}_{timestamp}.png
```

---

## Datos de Prueba

Las credenciales utilizadas para las pruebas parametrizadas se encuentran en `datos/users.json`. Este archivo contiene diferentes conjuntos de usuarios (validos, invalidos, bloqueados) que alimentan los tests de login.

Las credenciales son publicas y forman parte del sitio de demostracion SauceDemo. No representan datos sensibles reales.

---

## Disenio y Arquitectura

### Page Object Model (POM)

El proyecto implementa el patron Page Object Model para separar la logica de interaccion con la pagina de la logica de las pruebas:

- **BasePage**: Clase base que contiene metodos comunes (esperas, clics, envio de texto, validaciones)
- **LoginPage**: Interacciones con el formulario de inicio de sesion
- **InventoryPage**: Interacciones con el catalogo de productos
- **CartPage**: Interacciones con el carrito de compras
- **CheckoutPage**: Interacciones con el proceso de checkout

### Buenas Practicas

- Esperas explicitas (WebDriverWait) en lugar de time.sleep()
- Cada test tiene su propio driver (scope function) para garantizar aislamiento
- Datos de prueba externos en formato JSON
- Logging detallado en Page Objects y tests
- Capturas de pantalla automaticas ante fallos

---

## Integracion Continua (CI/CD)

El proyecto incluye un pipeline de GitHub Actions (`.github/workflows/pytest.yml`) que:

- Ejecuta la suite de pruebas automaticamente en cada push
- Instala Python, Chrome y las dependencias necesarias
- Genera y almacena los reportes como artefactos de ejecucion

---

*Proyecto desarrollado para la Entrega Final de la materia Automatizacion QA.*
