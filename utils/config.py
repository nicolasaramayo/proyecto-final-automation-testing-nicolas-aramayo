# =============================================================================
# utils/config.py
# Módulo de configuración central del proyecto de automatización QA.
# Contiene todas las constantes, URLs, credenciales de prueba y localizadores
# de elementos de la interfaz de usuario de SauceDemo.
#
# Centralizar estas definiciones evita duplicación de código y facilita el
# mantenimiento: si un localizador cambia, solo se modifica en este archivo.
# =============================================================================

from selenium.webdriver.common.by import By


# =============================================================================
# URLS DEL SITIO
# =============================================================================
BASE_URL = 'https://www.saucedemo.com'
LOGIN_URL = 'https://www.saucedemo.com'
INVENTORY_URL = 'https://www.saucedemo.com/inventory.html'
CART_URL = 'https://www.saucedemo.com/cart.html'


# =============================================================================
# CREDENCIALES DE PRUEBA
# =============================================================================
# Usuario estándar: acceso completo y funcional al sitio
VALID_USER = 'standard_user'
VALID_PASSWORD = 'secret_sauce'

# Usuario bloqueado: para probar el caso de login fallido por cuenta bloqueada
LOCKED_USER = 'locked_out_user'


# =============================================================================
# TÍTULOS ESPERADOS DE PÁGINA
# =============================================================================
PAGE_TITLE_EXPECTED = 'Swag Labs'
INVENTORY_TITLE_EXPECTED = 'Products'


# =============================================================================
# TIEMPO DE ESPERA (segundos)
# Usado como valor por defecto en todas las esperas explícitas de helpers.py
# =============================================================================
TIMEOUT = 10


# =============================================================================
# CLASE LOCATORS
# Centraliza todos los selectores de elementos de la UI de SauceDemo.
# Se usan tuplas (By.X, 'valor') compatibles con WebDriverWait y find_element.
# =============================================================================
class Locators:
    """
    Clase de constantes con los localizadores de todos los elementos
    de interfaz usados en las pruebas automatizadas.

    Cada localizador es una tupla (By.ESTRATEGIA, 'valor') que puede
    pasarse directamente a find_element() o a los helpers de espera.
    """

    # ------------------------------------------------------------------
    # PÁGINA DE LOGIN
    # ------------------------------------------------------------------
    # Campo de texto para el nombre de usuario
    USERNAME_INPUT = (By.ID, 'user-name')

    # Campo de texto para la contraseña
    PASSWORD_INPUT = (By.ID, 'password')

    # Botón "Login"
    LOGIN_BUTTON = (By.ID, 'login-button')

    # Mensaje de error que aparece ante credenciales inválidas o cuenta bloqueada
    ERROR_MESSAGE = (By.CSS_SELECTOR, '[data-test="error"]')


    # ------------------------------------------------------------------
    # PÁGINA DE INVENTARIO (CATÁLOGO DE PRODUCTOS)
    # ------------------------------------------------------------------
    # Contenedor principal que envuelve toda la lista de productos
    INVENTORY_CONTAINER = (By.ID, 'inventory_container')

    # Título de la página del inventario ("Products")
    INVENTORY_TITLE = (By.CLASS_NAME, 'title')

    # Lista completa de productos
    PRODUCT_LIST = (By.CLASS_NAME, 'inventory_list')

    # Cada ítem individual de producto en el inventario
    PRODUCT_ITEMS = (By.CLASS_NAME, 'inventory_item')

    # Nombre de un producto individual
    PRODUCT_NAME = (By.CLASS_NAME, 'inventory_item_name')

    # Precio de un producto individual
    PRODUCT_PRICE = (By.CLASS_NAME, 'inventory_item_price')

    # Botón "Add to cart" dentro de cada tarjeta de producto
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, 'button.btn_inventory')

    # Menú hamburguesa (navegación principal)
    BURGER_MENU = (By.ID, 'react-burger-menu-btn')

    # Selector desplegable para ordenar productos
    SORT_CONTAINER = (By.CLASS_NAME, 'product_sort_container')


    # ------------------------------------------------------------------
    # CARRITO DE COMPRAS
    # ------------------------------------------------------------------
    # Ícono/badge del carrito que muestra la cantidad de ítems
    CART_BADGE = (By.CLASS_NAME, 'shopping_cart_badge')

    # Enlace al carrito de compras (ícono de carrito en el header)
    CART_LINK = (By.CLASS_NAME, 'shopping_cart_link')

    # Cada ítem individual dentro del carrito
    CART_ITEMS = (By.CLASS_NAME, 'cart_item')

    # Nombre del producto dentro del carrito
    CART_ITEM_NAME = (By.CLASS_NAME, 'inventory_item_name')

    # Botón "Checkout" en el carrito
    CHECKOUT_BUTTON = (By.ID, 'checkout')

    # ------------------------------------------------------------------
    # PÁGINA DE CHECKOUT (PASO 1: INFORMACIÓN DEL CLIENTE)
    # ------------------------------------------------------------------
    FIRST_NAME_INPUT = (By.ID, 'first-name')
    LAST_NAME_INPUT = (By.ID, 'last-name')
    POSTAL_CODE_INPUT = (By.ID, 'postal-code')
    CONTINUE_BUTTON = (By.ID, 'continue')

    # ------------------------------------------------------------------
    # PÁGINA DE CHECKOUT (PASO 2: VISTA PREVIA Y FINALIZACIÓN)
    # ------------------------------------------------------------------
    FINISH_BUTTON = (By.ID, 'finish')
    COMPLETE_HEADER = (By.CLASS_NAME, 'complete-header')
