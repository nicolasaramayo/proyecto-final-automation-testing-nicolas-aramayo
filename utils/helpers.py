# =============================================================================
# utils/helpers.py
# Módulo de funciones de utilidad reutilizables para el proyecto QA.
#
# Proporciona:
#   - Funciones de espera explícita (WebDriverWait) para distintas condiciones.
#   - Función de login reutilizable para todos los tests que la requieran.
#   - Función para tomar screenshots manualmente.
#   - Funciones para interactuar con el catálogo de productos y el carrito.
#
# NOTA: Ninguna función usa time.sleep(). Se utilizan únicamente esperas
# explícitas con WebDriverWait para garantizar robustez y velocidad óptima.
# =============================================================================

import os
import logging
from datetime import datetime

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from utils.config import (
    BASE_URL,
    TIMEOUT,
    Locators,
)

# Logger del módulo
logger = logging.getLogger(__name__)


# =============================================================================
# FUNCIONES DE ESPERA EXPLÍCITA
# =============================================================================

def wait_for_element(driver, locator, timeout=TIMEOUT):
    """
    Espera hasta que un elemento esté PRESENTE en el DOM de la página.

    No implica que el elemento sea visible o interactuable; solo confirma
    que existe en el árbol HTML. Útil para verificar carga de elementos.

    Args:
        driver:  Instancia activa del WebDriver de Selenium.
        locator: Tupla (By.X, 'valor') que identifica al elemento.
        timeout: Segundos máximos de espera (default: TIMEOUT de config.py).

    Returns:
        WebElement: El elemento encontrado.

    Raises:
        TimeoutException: Si el elemento no aparece dentro del timeout.
    """
    logger.debug(f"Esperando presencia de elemento: {locator}")
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(locator),
        message=f"Timeout: el elemento {locator} no fue encontrado en {timeout}s."
    )


def wait_for_element_clickable(driver, locator, timeout=TIMEOUT):
    """
    Espera hasta que un elemento esté VISIBLE y sea CLICKEABLE.

    Más estricto que wait_for_element: garantiza que el elemento está
    listo para la interacción del usuario (no oculto ni deshabilitado).

    Args:
        driver:  Instancia activa del WebDriver de Selenium.
        locator: Tupla (By.X, 'valor') que identifica al elemento.
        timeout: Segundos máximos de espera (default: TIMEOUT de config.py).

    Returns:
        WebElement: El elemento listo para ser clickeado.

    Raises:
        TimeoutException: Si el elemento no es clickeable dentro del timeout.
    """
    logger.debug(f"Esperando que el elemento sea clickeable: {locator}")
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(locator),
        message=f"Timeout: el elemento {locator} no fue clickeable en {timeout}s."
    )


def wait_for_url_contains(driver, url_fragment, timeout=TIMEOUT):
    """
    Espera hasta que la URL actual del navegador CONTENGA el fragmento dado.

    Muy útil para verificar redirecciones de página luego de acciones
    como login, agregar al carrito, o navegar a checkout.

    Args:
        driver:       Instancia activa del WebDriver de Selenium.
        url_fragment: Subcadena que debe estar presente en la URL actual.
        timeout:      Segundos máximos de espera (default: TIMEOUT de config.py).

    Returns:
        bool: True si la URL contiene el fragmento dentro del timeout.

    Raises:
        TimeoutException: Si la URL no contiene el fragmento a tiempo.
    """
    logger.debug(f"Esperando que la URL contenga: '{url_fragment}'")
    return WebDriverWait(driver, timeout).until(
        EC.url_contains(url_fragment),
        message=f"Timeout: la URL no contiene '{url_fragment}' luego de {timeout}s."
    )


def wait_for_text_in_element(driver, locator, text, timeout=TIMEOUT):
    """
    Espera hasta que el TEXTO dado esté presente dentro de un elemento.

    Útil para confirmar que contenido dinámico (cargado por AJAX o JS)
    ya fue renderizado con el valor esperado.

    Args:
        driver:  Instancia activa del WebDriver de Selenium.
        locator: Tupla (By.X, 'valor') que identifica al elemento.
        text:    Texto que debe aparecer dentro del elemento.
        timeout: Segundos máximos de espera (default: TIMEOUT de config.py).

    Returns:
        bool: True si el texto está presente dentro del timeout.

    Raises:
        TimeoutException: Si el texto no aparece a tiempo.
    """
    logger.debug(f"Esperando texto '{text}' en elemento: {locator}")
    return WebDriverWait(driver, timeout).until(
        EC.text_to_be_present_in_element(locator, text),
        message=f"Timeout: el texto '{text}' no apareció en {locator} en {timeout}s."
    )


# =============================================================================
# FUNCIÓN DE LOGIN
# =============================================================================

def do_login(driver, username, password):
    """
    Realiza el flujo completo de inicio de sesión en SauceDemo.

    Pasos:
      1. Navega a la URL base (página de login).
      2. Espera a que el campo de usuario sea interactuable.
      3. Limpia e ingresa el nombre de usuario.
      4. Limpia e ingresa la contraseña.
      5. Hace clic en el botón de login.

    Args:
        driver:   Instancia activa del WebDriver de Selenium.
        username: Nombre de usuario a ingresar.
        password: Contraseña a ingresar.

    Note:
        Esta función NO verifica si el login fue exitoso; eso debe
        hacerse en el test mediante asserts después de llamar a do_login().
    """
    logger.info(f"Iniciando sesión con usuario: '{username}'")

    # 1. Navegar a la página de login
    driver.get(BASE_URL)
    logger.info(f"Navegado a: {BASE_URL}")

    # 2. Esperar y completar campo de usuario
    username_field = wait_for_element_clickable(driver, Locators.USERNAME_INPUT)
    username_field.clear()
    username_field.send_keys(username)
    logger.debug(f"Usuario ingresado: '{username}'")

    # 3. Esperar y completar campo de contraseña
    password_field = wait_for_element_clickable(driver, Locators.PASSWORD_INPUT)
    password_field.clear()
    password_field.send_keys(password)
    logger.debug("Contraseña ingresada.")

    # 4. Hacer clic en el botón de login
    login_button = wait_for_element_clickable(driver, Locators.LOGIN_BUTTON)
    login_button.click()
    logger.info("Botón de login clickeado.")


# =============================================================================
# FUNCIÓN DE CAPTURA DE PANTALLA MANUAL
# =============================================================================

def take_screenshot(driver, name):
    """
    Toma una captura de pantalla del estado actual del navegador y la guarda
    en el directorio reports/screenshots/.

    El nombre del archivo incluye el nombre dado y un timestamp para
    garantizar que no se sobreescriban capturas anteriores.

    Args:
        driver: Instancia activa del WebDriver de Selenium.
        name:   Nombre descriptivo para identificar la screenshot.

    Returns:
        str: Ruta absoluta del archivo guardado.
    """
    # Crear el directorio si no existe
    screenshots_dir = os.path.join("reports", "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    # Construir nombre de archivo con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Sanitizar el nombre: reemplazar espacios y caracteres problemáticos
    safe_name = name.replace(" ", "_").replace("/", "_").replace(":", "_")
    filename = f"{safe_name}_{timestamp}.png"
    filepath = os.path.join(screenshots_dir, filename)

    # Guardar la captura
    driver.save_screenshot(filepath)
    logger.info(f"Screenshot guardada: {filepath}")

    return filepath


# =============================================================================
# FUNCIONES DE INTERACCIÓN CON EL CATÁLOGO
# =============================================================================

def get_all_products(driver):
    """
    Obtiene la información de todos los productos visibles en la página
    de inventario y los retorna como una lista de diccionarios.

    Cada diccionario tiene las claves:
      - 'name':  Nombre del producto (str).
      - 'price': Precio del producto con símbolo '$' (str).

    Args:
        driver: Instancia activa del WebDriver, posicionado en la página
                de inventario (/inventory.html).

    Returns:
        list[dict]: Lista de productos con 'name' y 'price'.
                    Retorna lista vacía si no hay productos visibles.

    Example:
        >>> products = get_all_products(driver)
        >>> print(products[0])
        {'name': 'Sauce Labs Backpack', 'price': '$29.99'}
    """
    logger.info("Obteniendo lista de todos los productos del inventario.")

    # Esperar a que la lista de productos esté presente
    wait_for_element(driver, Locators.PRODUCT_LIST)

    # Obtener todos los ítems de producto
    product_items = driver.find_elements(*Locators.PRODUCT_ITEMS)
    logger.info(f"Se encontraron {len(product_items)} producto(s) en el inventario.")

    products = []
    for index, item in enumerate(product_items):
        try:
            # Extraer nombre del producto desde el ítem actual
            name_element = item.find_element(*Locators.PRODUCT_NAME)
            name = name_element.text.strip()

            # Extraer precio del producto desde el ítem actual
            price_element = item.find_element(*Locators.PRODUCT_PRICE)
            price = price_element.text.strip()

            products.append({'name': name, 'price': price})
            logger.debug(f"Producto {index + 1}: '{name}' -> {price}")

        except Exception as e:
            logger.warning(f"Error al leer producto en índice {index}: {e}")
            continue

    return products


def add_first_product_to_cart(driver):
    """
    Agrega el PRIMER producto visible del inventario al carrito de compras.

    Espera a que los botones "Add to cart" estén presentes y hace clic
    en el primero disponible. Retorna el nombre del producto agregado
    para que el test pueda verificar que aparece en el carrito.

    Args:
        driver: Instancia activa del WebDriver, posicionado en la página
                de inventario (/inventory.html).

    Returns:
        str: Nombre del primer producto agregado al carrito.

    Raises:
        TimeoutException: Si no hay productos disponibles en la página.
    """
    logger.info("Agregando el primer producto al carrito.")

    # Esperar a que haya al menos un ítem de producto disponible
    wait_for_element(driver, Locators.PRODUCT_ITEMS)

    # Obtener el primer ítem de producto
    first_product = driver.find_elements(*Locators.PRODUCT_ITEMS)[0]

    # Obtener el nombre del producto antes de agregarlo (para verificación posterior)
    product_name = first_product.find_element(*Locators.PRODUCT_NAME).text.strip()
    logger.info(f"Producto seleccionado: '{product_name}'")

    # Hacer clic en el botón "Add to cart" del primer producto
    add_button = first_product.find_element(*Locators.ADD_TO_CART_BUTTON)
    add_button.click()
    logger.info(f"Producto '{product_name}' agregado al carrito.")

    return product_name
