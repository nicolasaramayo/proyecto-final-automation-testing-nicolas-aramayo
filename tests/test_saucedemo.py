# =============================================================================
# tests/test_saucedemo.py
# Suite de pruebas automatizadas para el sitio https://www.saucedemo.com
#
# Organización en 3 clases de prueba:
#   - TestLogin:   Verifica el comportamiento del formulario de inicio de sesión.
#   - TestCatalog: Verifica la visualización correcta del catálogo de productos.
#   - TestCart:    Verifica la funcionalidad de agregar productos al carrito.
#
# Convenciones:
#   - Cada test usa el fixture `driver` definido en conftest.py.
#   - Los tests que requieren sesión iniciada usan do_login() de helpers.py.
#   - Se usan esperas explícitas de helpers.py; NUNCA time.sleep().
#   - Cada assert incluye un mensaje descriptivo para diagnóstico en reportes.
#   - Se usa logging para registrar el flujo de ejecución de cada test.
# =============================================================================

import logging
import pytest

from utils.config import (
    VALID_USER,
    VALID_PASSWORD,
    LOCKED_USER,
    INVENTORY_URL,
    CART_URL,
    INVENTORY_TITLE_EXPECTED,
    PAGE_TITLE_EXPECTED,
    Locators,
)
from utils.helpers import (
    do_login,
    wait_for_element,
    wait_for_element_clickable,
    wait_for_url_contains,
    wait_for_text_in_element,
    add_first_product_to_cart,
    get_all_products,
)

# Logger compartido para todos los tests de este módulo
logger = logging.getLogger(__name__)


# =============================================================================
# CLASE 1: TestLogin
# Pruebas relacionadas con el formulario de inicio de sesión de SauceDemo.
# Cubre: login exitoso, login fallido y presencia de elementos del formulario.
# =============================================================================
class TestLogin:
    """
    Suite de pruebas para la página de login de SauceDemo.

    Verifica que:
      - Un usuario válido puede iniciar sesión exitosamente.
      - Las credenciales inválidas muestran un mensaje de error.
      - Los elementos del formulario de login están presentes en la página.
    """

    def test_successful_login(self, driver):
        """
        CASO DE PRUEBA: Login exitoso con credenciales válidas.

        Precondición:
            El usuario no está autenticado.

        Pasos:
            1. Navegar a la página de login (BASE_URL).
            2. Ingresar usuario y contraseña válidos.
            3. Hacer clic en el botón "Login".

        Resultado esperado:
            - La URL cambia a '/inventory.html' (redirección post-login).
            - El título de la página contiene 'Products' o 'Swag Labs'.
        """
        logger.info("TEST: test_successful_login - Inicio")

        # Ejecutar el flujo de login con credenciales válidas
        do_login(driver, VALID_USER, VALID_PASSWORD)

        # Verificar 1: La URL debe contener '/inventory.html' tras el login exitoso
        wait_for_url_contains(driver, '/inventory.html')
        current_url = driver.current_url
        logger.info(f"URL actual después del login: {current_url}")

        assert '/inventory.html' in current_url, (
            f"ERROR: Se esperaba redirección a '/inventory.html', "
            f"pero la URL actual es: '{current_url}'"
        )

        # Verificar 2: El título visible de la página debe ser 'Products'
        title_element = wait_for_element(driver, Locators.INVENTORY_TITLE)
        page_title = title_element.text.strip()
        logger.info(f"Título de página encontrado: '{page_title}'")

        assert INVENTORY_TITLE_EXPECTED in page_title or PAGE_TITLE_EXPECTED in driver.title, (
            f"ERROR: Se esperaba título '{INVENTORY_TITLE_EXPECTED}', "
            f"pero se encontró: '{page_title}'"
        )

        logger.info("TEST: test_successful_login - EXITOSO ✓")

    def test_login_with_invalid_credentials(self, driver):
        """
        CASO DE PRUEBA: Login fallido con contraseña incorrecta.

        Precondición:
            El usuario no está autenticado.

        Pasos:
            1. Navegar a la página de login.
            2. Ingresar un usuario válido con contraseña INCORRECTA.
            3. Hacer clic en el botón "Login".

        Resultado esperado:
            - Se muestra un mensaje de error visible en pantalla.
            - El mensaje de error no está vacío.
            - El usuario NO es redirigido al inventario.
        """
        logger.info("TEST: test_login_with_invalid_credentials - Inicio")

        # Intentar login con contraseña incorrecta
        do_login(driver, VALID_USER, 'contraseña_incorrecta_123')

        # Verificar que el mensaje de error es visible
        error_element = wait_for_element(driver, Locators.ERROR_MESSAGE)
        error_text = error_element.text.strip()
        logger.info(f"Mensaje de error obtenido: '{error_text}'")

        # El mensaje de error debe existir y no estar vacío
        assert error_element.is_displayed(), (
            "ERROR: El elemento de mensaje de error no está visible."
        )
        assert len(error_text) > 0, (
            "ERROR: El mensaje de error está vacío, se esperaba un texto de error."
        )

        # El usuario NO debe haber sido redirigido al inventario
        current_url = driver.current_url
        assert '/inventory.html' not in current_url, (
            f"ERROR: El usuario fue redirigido al inventario con credenciales inválidas. "
            f"URL actual: '{current_url}'"
        )

        logger.info(f"Mensaje de error verificado: '{error_text}'")
        logger.info("TEST: test_login_with_invalid_credentials - EXITOSO ✓")

    def test_login_fields_present(self, driver):
        """
        CASO DE PRUEBA: Verificación de presencia de elementos del formulario de login.

        Precondición:
            El usuario no está autenticado.

        Pasos:
            1. Navegar a la página de login (sin iniciar sesión).

        Resultado esperado:
            - El campo de nombre de usuario está presente y visible.
            - El campo de contraseña está presente y visible.
            - El botón "Login" está presente y visible.
        """
        logger.info("TEST: test_login_fields_present - Inicio")

        # Navegar a la página de login sin ingresar credenciales
        from utils.config import BASE_URL
        driver.get(BASE_URL)
        logger.info(f"Navegado a la página de login: {BASE_URL}")

        # Verificar presencia y visibilidad del campo de usuario
        username_field = wait_for_element(driver, Locators.USERNAME_INPUT)
        assert username_field.is_displayed(), (
            "ERROR: El campo de nombre de usuario no está visible en la página."
        )
        logger.info("Campo de usuario: PRESENTE ✓")

        # Verificar presencia y visibilidad del campo de contraseña
        password_field = wait_for_element(driver, Locators.PASSWORD_INPUT)
        assert password_field.is_displayed(), (
            "ERROR: El campo de contraseña no está visible en la página."
        )
        logger.info("Campo de contraseña: PRESENTE ✓")

        # Verificar presencia y visibilidad del botón de login
        login_button = wait_for_element(driver, Locators.LOGIN_BUTTON)
        assert login_button.is_displayed(), (
            "ERROR: El botón 'Login' no está visible en la página."
        )
        logger.info("Botón de login: PRESENTE ✓")

        logger.info("TEST: test_login_fields_present - EXITOSO ✓")


# =============================================================================
# CLASE 2: TestCatalog
# Pruebas del catálogo de productos (página de inventario) de SauceDemo.
# Verifica la visualización, cantidad, y datos de los productos.
# =============================================================================
class TestCatalog:
    """
    Suite de pruebas para la página de inventario/catálogo de SauceDemo.

    Verifica que:
      - El título de la página de inventario es correcto.
      - Se muestran los productos esperados.
      - Los elementos de UI del catálogo están presentes (menú, filtro, carrito).
      - El primer producto tiene nombre e información de precio válidos.
    """

    def test_inventory_page_title(self, driver):
        """
        CASO DE PRUEBA: El título de la página de inventario es 'Products'.

        Precondición:
            Usuario no autenticado.

        Pasos:
            1. Iniciar sesión con credenciales válidas.
            2. Verificar que el elemento de título visible diga 'Products'.

        Resultado esperado:
            - El elemento <span class="title"> contiene el texto 'Products'.
        """
        logger.info("TEST: test_inventory_page_title - Inicio")

        # Iniciar sesión para acceder al inventario
        do_login(driver, VALID_USER, VALID_PASSWORD)

        # Esperar a que el título sea visible y contenga 'Products'
        wait_for_text_in_element(driver, Locators.INVENTORY_TITLE, INVENTORY_TITLE_EXPECTED)

        # Obtener el texto del título y verificarlo
        title_element = wait_for_element(driver, Locators.INVENTORY_TITLE)
        title_text = title_element.text.strip()
        logger.info(f"Título de inventario encontrado: '{title_text}'")

        assert INVENTORY_TITLE_EXPECTED in title_text, (
            f"ERROR: Se esperaba el título '{INVENTORY_TITLE_EXPECTED}', "
            f"pero se encontró: '{title_text}'"
        )

        logger.info("TEST: test_inventory_page_title - EXITOSO ✓")

    def test_products_are_visible(self, driver):
        """
        CASO DE PRUEBA: Se muestran productos en la página de inventario.

        Precondición:
            Usuario no autenticado.

        Pasos:
            1. Iniciar sesión con credenciales válidas.
            2. Contar los ítems de producto visibles en la página.

        Resultado esperado:
            - Hay al menos 1 producto visible (SauceDemo muestra exactamente 6).
        """
        logger.info("TEST: test_products_are_visible - Inicio")

        # Iniciar sesión
        do_login(driver, VALID_USER, VALID_PASSWORD)

        # Esperar a que el contenedor de inventario esté presente
        wait_for_element(driver, Locators.INVENTORY_CONTAINER)

        # Obtener todos los ítems de producto
        product_items = driver.find_elements(*Locators.PRODUCT_ITEMS)
        product_count = len(product_items)
        logger.info(f"Cantidad de productos encontrados: {product_count}")

        # SauceDemo tiene 6 productos por defecto
        assert product_count >= 1, (
            f"ERROR: Se esperaba al menos 1 producto en el inventario, "
            f"pero se encontraron: {product_count}"
        )

        # Verificación adicional: idealmente deben ser 6 productos
        assert product_count == 6, (
            f"ADVERTENCIA: Se esperaban 6 productos (catálogo completo de SauceDemo), "
            f"pero se encontraron: {product_count}"
        )

        logger.info(f"Cantidad de productos verificada: {product_count} ✓")
        logger.info("TEST: test_products_are_visible - EXITOSO ✓")

    def test_ui_elements_present(self, driver):
        """
        CASO DE PRUEBA: Los elementos de UI del catálogo están presentes.

        Precondición:
            Usuario no autenticado.

        Pasos:
            1. Iniciar sesión con credenciales válidas.
            2. Verificar presencia del menú hamburguesa.
            3. Verificar presencia del selector de ordenamiento.
            4. Verificar presencia del ícono del carrito.

        Resultado esperado:
            - Los tres elementos de UI están visibles en la página.
        """
        logger.info("TEST: test_ui_elements_present - Inicio")

        # Iniciar sesión
        do_login(driver, VALID_USER, VALID_PASSWORD)

        # Esperar a que la página de inventario cargue
        wait_for_element(driver, Locators.INVENTORY_CONTAINER)

        # Verificar el menú hamburguesa (navegación principal)
        burger_menu = wait_for_element(driver, Locators.BURGER_MENU)
        assert burger_menu.is_displayed(), (
            "ERROR: El menú hamburguesa no está visible en la página de inventario."
        )
        logger.info("Menú hamburguesa: PRESENTE ✓")

        # Verificar el selector de ordenamiento de productos
        sort_filter = wait_for_element(driver, Locators.SORT_CONTAINER)
        assert sort_filter.is_displayed(), (
            "ERROR: El selector de ordenamiento no está visible en la página de inventario."
        )
        logger.info("Selector de ordenamiento: PRESENTE ✓")

        # Verificar el ícono del carrito en el header
        cart_link = wait_for_element(driver, Locators.CART_LINK)
        assert cart_link.is_displayed(), (
            "ERROR: El ícono del carrito no está visible en la página de inventario."
        )
        logger.info("Ícono del carrito: PRESENTE ✓")

        logger.info("TEST: test_ui_elements_present - EXITOSO ✓")

    def test_first_product_info(self, driver):
        """
        CASO DE PRUEBA: El primer producto tiene nombre e información de precio válidos.

        Precondición:
            Usuario no autenticado.

        Pasos:
            1. Iniciar sesión con credenciales válidas.
            2. Obtener la información del primer producto del catálogo.
            3. Verificar que el nombre no está vacío.
            4. Verificar que el precio empieza con '$'.

        Resultado esperado:
            - El primer producto tiene un nombre con al menos 1 carácter.
            - El precio del primer producto comienza con el símbolo '$'.
        """
        logger.info("TEST: test_first_product_info - Inicio")

        # Iniciar sesión
        do_login(driver, VALID_USER, VALID_PASSWORD)

        # Esperar a que la lista de productos esté visible
        wait_for_element(driver, Locators.PRODUCT_LIST)

        # Obtener todos los productos
        products = get_all_products(driver)

        # Debe haber al menos un producto
        assert len(products) > 0, (
            "ERROR: No se encontraron productos en el inventario."
        )

        # Inspeccionar el primer producto
        first_product = products[0]
        product_name = first_product['name']
        product_price = first_product['price']

        logger.info(f"Primer producto - Nombre: '{product_name}' | Precio: '{product_price}'")

        # El nombre no debe estar vacío
        assert len(product_name) > 0, (
            "ERROR: El nombre del primer producto está vacío."
        )

        # El precio debe comenzar con el símbolo '$' (formato de moneda USD)
        assert product_price.startswith('$'), (
            f"ERROR: El precio del primer producto no comienza con '$'. "
            f"Precio encontrado: '{product_price}'"
        )

        logger.info(f"Información del primer producto verificada: '{product_name}' -> {product_price} ✓")
        logger.info("TEST: test_first_product_info - EXITOSO ✓")


# =============================================================================
# CLASE 3: TestCart
# Pruebas de la funcionalidad del carrito de compras de SauceDemo.
# Verifica agregar productos, el badge del carrito y la navegación al carrito.
# =============================================================================
class TestCart:
    """
    Suite de pruebas para la funcionalidad del carrito de SauceDemo.

    Verifica que:
      - Al agregar un producto, el badge del carrito muestra '1'.
      - El producto agregado aparece correctamente en la vista del carrito.
      - La navegación al carrito lleva a la URL correcta.
    """

    def test_add_product_to_cart(self, driver):
        """
        CASO DE PRUEBA: Agregar el primer producto al carrito actualiza el badge.

        Precondición:
            Usuario no autenticado.

        Pasos:
            1. Iniciar sesión con credenciales válidas.
            2. Agregar el primer producto al carrito usando la función helper.
            3. Verificar que el badge del carrito muestra el número '1'.

        Resultado esperado:
            - El badge rojo del carrito en el header muestra el valor '1'.
        """
        logger.info("TEST: test_add_product_to_cart - Inicio")

        # Iniciar sesión y navegar al inventario
        do_login(driver, VALID_USER, VALID_PASSWORD)
        wait_for_element(driver, Locators.INVENTORY_CONTAINER)

        # Agregar el primer producto al carrito
        product_name = add_first_product_to_cart(driver)
        logger.info(f"Producto agregado: '{product_name}'")

        # Esperar a que el badge del carrito sea visible
        cart_badge = wait_for_element(driver, Locators.CART_BADGE)
        badge_count = cart_badge.text.strip()
        logger.info(f"Badge del carrito muestra: '{badge_count}'")

        # El badge debe mostrar '1' (un solo producto agregado)
        assert badge_count == '1', (
            f"ERROR: El badge del carrito debería mostrar '1', "
            f"pero muestra: '{badge_count}'"
        )

        logger.info("TEST: test_add_product_to_cart - EXITOSO ✓")

    def test_product_appears_in_cart(self, driver):
        """
        CASO DE PRUEBA: El producto agregado aparece en la vista del carrito.

        Precondición:
            Usuario no autenticado.

        Pasos:
            1. Iniciar sesión con credenciales válidas.
            2. Agregar el primer producto al carrito.
            3. Hacer clic en el ícono del carrito para navegar a la vista del carrito.
            4. Verificar que el nombre del producto aparece en la lista del carrito.

        Resultado esperado:
            - La página del carrito contiene al menos 1 ítem.
            - El nombre del producto agregado coincide con el que aparece en el carrito.
        """
        logger.info("TEST: test_product_appears_in_cart - Inicio")

        # Iniciar sesión
        do_login(driver, VALID_USER, VALID_PASSWORD)
        wait_for_element(driver, Locators.INVENTORY_CONTAINER)

        # Agregar el primer producto y guardar su nombre para verificación
        product_name = add_first_product_to_cart(driver)
        logger.info(f"Producto agregado al carrito: '{product_name}'")

        # Hacer clic en el ícono del carrito para ir a la vista del carrito
        cart_link = wait_for_element_clickable(driver, Locators.CART_LINK)
        cart_link.click()
        logger.info("Navegado a la vista del carrito.")

        # Esperar a que la URL del carrito cargue
        wait_for_url_contains(driver, '/cart.html')

        # Esperar a que aparezca al menos un ítem en el carrito
        wait_for_element(driver, Locators.CART_ITEMS)

        # Obtener todos los ítems del carrito
        cart_items = driver.find_elements(*Locators.CART_ITEMS)
        cart_item_count = len(cart_items)
        logger.info(f"Ítems encontrados en el carrito: {cart_item_count}")

        # Debe haber al menos 1 ítem
        assert cart_item_count >= 1, (
            f"ERROR: Se esperaba al menos 1 ítem en el carrito, "
            f"pero se encontraron: {cart_item_count}"
        )

        # Verificar que el nombre del producto coincide con el que agregamos
        cart_item_name_element = cart_items[0].find_element(*Locators.CART_ITEM_NAME)
        cart_item_name = cart_item_name_element.text.strip()
        logger.info(f"Nombre del producto en carrito: '{cart_item_name}'")

        assert cart_item_name == product_name, (
            f"ERROR: El nombre del producto en el carrito ('{cart_item_name}') "
            f"no coincide con el producto agregado ('{product_name}')."
        )

        logger.info("TEST: test_product_appears_in_cart - EXITOSO ✓")

    def test_cart_navigation(self, driver):
        """
        CASO DE PRUEBA: La navegación al carrito lleva a la URL correcta.

        Precondición:
            Usuario no autenticado.

        Pasos:
            1. Iniciar sesión con credenciales válidas.
            2. Agregar un producto al carrito.
            3. Hacer clic en el ícono del carrito.
            4. Verificar que la URL resultante es la URL del carrito.

        Resultado esperado:
            - La URL del navegador corresponde a '/cart.html' (CART_URL de config.py).
        """
        logger.info("TEST: test_cart_navigation - Inicio")

        # Iniciar sesión
        do_login(driver, VALID_USER, VALID_PASSWORD)
        wait_for_element(driver, Locators.INVENTORY_CONTAINER)

        # Agregar un producto (necesario para que el carrito tenga contenido)
        product_name = add_first_product_to_cart(driver)
        logger.info(f"Producto agregado para la prueba: '{product_name}'")

        # Hacer clic en el ícono del carrito
        cart_link = wait_for_element_clickable(driver, Locators.CART_LINK)
        cart_link.click()

        # Esperar que la URL cambie a la página del carrito
        wait_for_url_contains(driver, '/cart.html')

        # Verificar la URL actual del navegador
        current_url = driver.current_url
        logger.info(f"URL actual después de navegar al carrito: {current_url}")

        assert CART_URL in current_url or '/cart.html' in current_url, (
            f"ERROR: Se esperaba la URL del carrito ('{CART_URL}'), "
            f"pero la URL actual es: '{current_url}'"
        )

        logger.info("TEST: test_cart_navigation - EXITOSO ✓")
