import os
import json
import logging
import pytest

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

logger = logging.getLogger(__name__)

def load_users(key):
    """Carga los datos de usuarios desde datos/users.json."""
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datos', 'users.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data[key]

# =============================================================================
# SUITE DE PRUEBAS DE INTERFAZ DE USUARIO (UI)
# =============================================================================

def test_successful_login(driver):
    """
    CASO DE PRUEBA: Login exitoso con credenciales válidas.
    Verifica la redirección y el título del inventario.
    """
    logger.info("Iniciando test_successful_login")
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    login_page.navigate()
    valid_user = load_users("valid_users")[0]
    login_page.login(valid_user["username"], valid_user["password"])

    inventory_page.wait_for_url_contains("/inventory.html")
    assert "/inventory.html" in driver.current_url, "No se redirigió a la página de inventario."
    
    title = inventory_page.get_title_text()
    assert title == "Products", f"Título incorrecto: {title}"
    logger.info("test_successful_login finalizado con éxito.")


@pytest.mark.parametrize("invalid_user_data", load_users("invalid_users"))
def test_failed_login(driver, invalid_user_data):
    """
    CASO DE PRUEBA: Login fallido parametrizado.
    Verifica que se muestren los mensajes de error correspondientes para usuarios bloqueados/inválidos.
    """
    logger.info(f"Iniciando test_failed_login para caso: {invalid_user_data['description']}")
    login_page = LoginPage(driver)

    login_page.navigate()
    login_page.login(invalid_user_data["username"], invalid_user_data["password"])

    assert login_page.is_error_displayed(), "El mensaje de error no se mostró."
    error_text = login_page.get_error_message()
    assert invalid_user_data["error_message"] in error_text, f"Mensaje de error inesperado: '{error_text}'"
    logger.info("test_failed_login validado correctamente.")


def test_catalog_elements_and_count(driver):
    """
    CASO DE PRUEBA: Validación de elementos del catálogo y cantidad.
    Verifica visibilidad de barra lateral, filtro, carrito, y cuenta exacta de 6 productos.
    """
    logger.info("Iniciando test_catalog_elements_and_count")
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    login_page.navigate()
    valid_user = load_users("valid_users")[0]
    login_page.login(valid_user["username"], valid_user["password"])

    inventory_page.wait_for_url_contains("/inventory.html")
    assert inventory_page.is_burger_menu_displayed(), "El menú hamburguesa no está visible."
    assert inventory_page.is_sort_container_displayed(), "El filtro de ordenamiento no está visible."
    assert inventory_page.is_cart_link_displayed(), "El ícono del carrito no está visible."

    count = inventory_page.get_product_count()
    assert count == 6, f"Se esperaban 6 productos, pero se encontraron {count}."
    logger.info("test_catalog_elements_and_count finalizado con éxito.")


def test_add_to_cart_updates_badge(driver):
    """
    CASO DE PRUEBA: Agregar al carrito actualiza badge.
    Verifica que el badge incremente de vacío a '1'.
    """
    logger.info("Iniciando test_add_to_cart_updates_badge")
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    login_page.navigate()
    valid_user = load_users("valid_users")[0]
    login_page.login(valid_user["username"], valid_user["password"])

    inventory_page.wait_for_url_contains("/inventory.html")
    badge_before = inventory_page.get_cart_badge_count()
    assert badge_before == "", "El badge del carrito no esta vacio al inicio."

    inventory_page.add_first_product_to_cart()
    badge_after = inventory_page.wait_for_cart_badge("1")
    assert badge_after == "1", f"El badge del carrito muestra '{badge_after}', se esperaba '1'."
    logger.info("test_add_to_cart_updates_badge finalizado con éxito.")


def test_complete_checkout_flow(driver):
    """
    CASO DE PRUEBA: Flujo completo de compra (E2E).
    Verifica login -> catálogo -> carrito -> checkout -> confirmación.
    """
    logger.info("Iniciando test_complete_checkout_flow")
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)

    login_page.navigate()
    valid_user = load_users("valid_users")[0]
    login_page.login(valid_user["username"], valid_user["password"])

    inventory_page.wait_for_url_contains("/inventory.html")
    product_name = inventory_page.add_first_product_to_cart()
    inventory_page.go_to_cart()

    cart_page.wait_for_url_contains("/cart.html")
    cart_items = cart_page.get_cart_item_names()
    assert product_name in cart_items, f"El producto '{product_name}' no se encuentra en el carrito: {cart_items}"

    cart_page.click_checkout()
    
    checkout_page.wait_for_url_contains("/checkout-step-one.html")
    checkout_page.fill_client_details("John", "Doe", "12345")
    checkout_page.click_continue()

    checkout_page.wait_for_url_contains("/checkout-step-two.html")
    checkout_page.click_finish()

    checkout_page.wait_for_url_contains("/checkout-complete.html")
    success_msg = checkout_page.get_complete_header_text()
    assert "Thank you for your order" in success_msg, f"Mensaje final inesperado: '{success_msg}'"
    logger.info("test_complete_checkout_flow finalizado con éxito.")
