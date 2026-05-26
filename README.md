# 🧪 Pre-Entrega | Automatización QA - SauceDemo

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-8.2.0-green?logo=pytest&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-4.21.0-43B02A?logo=selenium&logoColor=white)
![WebDriver Manager](https://img.shields.io/badge/WebDriver--Manager-4.0.1-orange)

---

## 📋 Descripción del Proyecto

Este proyecto implementa una suite de pruebas automatizadas de extremo a extremo (**E2E**) sobre el sitio web de demostración **[SauceDemo](https://www.saucedemo.com)**, desarrollada como pre-entrega para la materia de Automatización QA.

Las pruebas cubren los flujos principales de la aplicación:
- ✅ **Login:** inicio de sesión exitoso, fallido y verificación de elementos del formulario.
- ✅ **Catálogo de Productos:** visualización de productos, título de página y elementos de UI.
- ✅ **Carrito de Compras:** agregar productos, verificar badge y navegación al carrito.

El proyecto sigue las buenas prácticas de automatización QA:
- **Esperas explícitas** (WebDriverWait) — sin `time.sleep()`.
- **Page Object-like helpers** centralizados en `utils/`.
- **Capturas de pantalla automáticas** ante fallos de tests.
- **Reporte HTML** generado automáticamente por `pytest-html`.

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|---|---|---|
| Python | 3.8+ | Lenguaje de programación principal |
| Selenium WebDriver | 4.21.0 | Automatización del navegador web |
| Pytest | 8.2.0 | Framework de ejecución de pruebas |
| pytest-html | 4.1.1 | Generación de reportes HTML |
| WebDriver Manager | 4.0.1 | Gestión automática de ChromeDriver |
| Google Chrome | Última versión | Navegador utilizado para las pruebas |

---

## 📁 Estructura del Proyecto

```
Pre-Entrega Automation QA/
│
├── conftest.py                  # Fixtures globales y hooks de Pytest
├── pytest.ini                   # Configuración de Pytest
├── requirements.txt             # Dependencias del proyecto
├── .gitignore                   # Archivos ignorados por Git
├── README.md                    # Este archivo
│
├── utils/                       # Módulos de utilidad reutilizables
│   ├── __init__.py
│   ├── config.py                # Constantes, URLs, credenciales y localizadores
│   └── helpers.py               # Funciones helper (login, esperas, screenshots)
│
├── tests/                       # Módulos de prueba
│   ├── __init__.py
│   └── test_saucedemo.py        # Suite completa de 10 tests (3 clases)
│
├── reports/                     # Reportes generados (creados al ejecutar tests)
│   ├── .gitkeep
│   ├── reporte.html             # Reporte HTML (generado por pytest-html)
│   └── screenshots/             # Capturas de pantalla ante fallos
│       └── .gitkeep
│
└── datos/                       # Directorio para datos de prueba (futuro uso)
    └── .gitkeep
```

---

## ⚙️ Instalación y Configuración

### Prerequisitos

Antes de comenzar, asegurarse de tener instalado:

- ✅ **Python 3.8 o superior** → [Descargar Python](https://www.python.org/downloads/)
- ✅ **Google Chrome** (versión actualizada) → [Descargar Chrome](https://www.google.com/chrome/)
- ✅ **Git** → [Descargar Git](https://git-scm.com/downloads)

Verificar instalación de Python:
```bash
python --version
```

### 1. Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd "Pre-Entrega Automation QA"
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

> Cuando el entorno está activo, verás `(venv)` al inicio del prompt.

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

> ℹ️ **WebDriver Manager** descargará automáticamente el ChromeDriver compatible con la versión de Chrome instalada. No es necesario descargarlo manualmente.

---

## 🚀 Ejecución de Pruebas

### Ejecutar todos los tests (con reporte HTML)

```bash
pytest
```

> El reporte se genera automáticamente en `reports/reporte.html` gracias a la configuración en `pytest.ini`.

### Ejecutar con reporte HTML especificando la ruta

```bash
pytest -v --html=reports/reporte.html --self-contained-html
```

### Ejecutar una clase específica de tests

```bash
# Solo los tests de Login
pytest tests/test_saucedemo.py::TestLogin -v

# Solo los tests del Catálogo
pytest tests/test_saucedemo.py::TestCatalog -v

# Solo los tests del Carrito
pytest tests/test_saucedemo.py::TestCart -v
```

### Ejecutar un test individual

```bash
pytest tests/test_saucedemo.py::TestLogin::test_successful_login -v
```

### Ver logs en consola durante la ejecución

```bash
pytest -v -s --log-cli-level=INFO
```

---

## 🧪 Casos de Prueba

| # | Test | Clase | Descripción |
|---|------|-------|-------------|
| 1 | `test_successful_login` | `TestLogin` | Verifica que un usuario válido puede iniciar sesión y es redirigido al inventario |
| 2 | `test_login_with_invalid_credentials` | `TestLogin` | Verifica que credenciales incorrectas muestran mensaje de error |
| 3 | `test_login_fields_present` | `TestLogin` | Verifica que el formulario de login tiene todos sus campos visibles |
| 4 | `test_inventory_page_title` | `TestCatalog` | Verifica que el título de la página de inventario es 'Products' |
| 5 | `test_products_are_visible` | `TestCatalog` | Verifica que se muestran los 6 productos del catálogo |
| 6 | `test_ui_elements_present` | `TestCatalog` | Verifica la presencia del menú, filtro de ordenamiento y carrito |
| 7 | `test_first_product_info` | `TestCatalog` | Verifica que el primer producto tiene nombre válido y precio en formato '$X.XX' |
| 8 | `test_add_product_to_cart` | `TestCart` | Verifica que al agregar un producto el badge del carrito muestra '1' |
| 9 | `test_product_appears_in_cart` | `TestCart` | Verifica que el producto agregado aparece correctamente en el carrito |
| 10 | `test_cart_navigation` | `TestCart` | Verifica que el ícono del carrito navega a la URL correcta (/cart.html) |

---

## 📊 Reportes

### Reporte HTML

Al ejecutar `pytest`, se genera automáticamente el archivo **`reports/reporte.html`**.

Para visualizarlo, abrir el archivo en cualquier navegador web:

```bash
# Windows
start reports\reporte.html

# macOS
open reports/reporte.html
```

El reporte incluye:
- ✅ Resumen de tests pasados, fallidos y omitidos
- 📋 Detalle de cada test con duración, logs y mensajes de error
- 🖼️ Referencias a capturas de pantalla (en caso de fallos)

### Capturas de Pantalla ante Fallos

Cuando un test **falla**, el hook `pytest_runtest_makereport` en `conftest.py` captura automáticamente una screenshot del estado del navegador en el momento del fallo.

Las imágenes se guardan en:
```
reports/screenshots/{nombre_del_test}_{timestamp}.png
```

---

## 👤 Credenciales de Prueba

| Tipo de Usuario | Usuario | Contraseña | Uso |
|---|---|---|---|
| Usuario estándar | `standard_user` | `secret_sauce` | Tests de login exitoso, catálogo y carrito |
| Usuario bloqueado | `locked_out_user` | `secret_sauce` | (Disponible en config.py para tests futuros) |

> ⚠️ Estas credenciales son públicas y forman parte del sitio de demostración SauceDemo. No representan datos sensibles reales.

---

## 📝 Notas

- 🌐 El navegador se abre en **modo visible** (`headless=False`) para que el evaluador pueda observar la ejecución de las pruebas en tiempo real.
- ⏱️ Las pruebas usan **esperas explícitas** (`WebDriverWait`) con un timeout de 10 segundos por defecto. No se usa `time.sleep()`.
- 🔄 Cada test tiene su **propio driver** (scope `function`) para garantizar aislamiento completo entre pruebas.
- 📦 **WebDriver Manager** gestiona ChromeDriver automáticamente; no es necesario descargarlo ni configurarlo manualmente.
- 🪟 El tamaño de ventana está fijo en **1280×800** píxeles para consistencia entre diferentes equipos y resoluciones.

---

*Proyecto desarrollado para la pre-entrega de la materia Automatización QA.*
