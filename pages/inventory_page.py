import logging
from pages.base_page import BasePage
from utils.config import Locators

logger = logging.getLogger(__name__)

class InventoryPage(BasePage):
    """
    Page Object para la página de Inventario/Catálogo de SauceDemo.
    """
    def get_title_text(self):
        """Retorna el texto del título de la página (ej. 'Products')."""
        return self.get_text(Locators.INVENTORY_TITLE)

    def get_product_count(self):
        """Retorna la cantidad de productos visibles en el catálogo."""
        self.wait_for_element(Locators.PRODUCT_LIST)
        items = self.driver.find_elements(*Locators.PRODUCT_ITEMS)
        return len(items)

    def get_all_products(self):
        """Retorna una lista de diccionarios con la información de todos los productos."""
        self.wait_for_element(Locators.PRODUCT_LIST)
        items = self.driver.find_elements(*Locators.PRODUCT_ITEMS)
        products = []
        for index, item in enumerate(items):
            try:
                name_element = item.find_element(*Locators.PRODUCT_NAME)
                name = name_element.text.strip()
                price_element = item.find_element(*Locators.PRODUCT_PRICE)
                price = price_element.text.strip()
                products.append({'name': name, 'price': price})
            except Exception as e:
                logger.warning(f"Error al leer producto en índice {index}: {e}")
        return products

    def add_first_product_to_cart(self):
        """Agrega el primer producto al carrito y retorna su nombre."""
        self.wait_for_element(Locators.PRODUCT_ITEMS)
        first_product = self.driver.find_elements(*Locators.PRODUCT_ITEMS)[0]
        product_name = first_product.find_element(*Locators.PRODUCT_NAME).text.strip()
        add_button = first_product.find_element(*Locators.ADD_TO_CART_BUTTON)
        # Usar JavaScript click para mayor compatibilidad en headless
        self.driver.execute_script("arguments[0].click();", add_button)
        logger.info(f"Producto '{product_name}' agregado al carrito.")
        return product_name

    def get_cart_badge_count(self):
        """Retorna el contador mostrado en el badge del carrito o una cadena vacia si no existe."""
        try:
            return self.get_text(Locators.CART_BADGE, timeout=3)
        except Exception as e:
            logger.debug(f"Badge no encontrado: {type(e).__name__}")
            return ""

    def wait_for_cart_badge(self, expected_count="1", timeout=10):
        """Espera a que el badge del carrito muestre el conteo esperado."""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element(Locators.CART_BADGE, expected_count),
            message=f"Badge del carrito no muestra '{expected_count}' en {timeout}s."
        )
        return self.get_text(Locators.CART_BADGE)

    def go_to_cart(self):
        """Navega a la pagina del carrito haciendo clic en el icono del carrito."""
        cart_link = self.wait_for_element_clickable(Locators.CART_LINK)
        # Usar JavaScript click para mayor compatibilidad en headless
        self.driver.execute_script("arguments[0].click();", cart_link)
        # Esperar a que la URL cambie a cart.html
        self.wait_for_url_contains("/cart.html")

    def is_burger_menu_displayed(self):
        """Verifica si el menú hamburguesa está visible."""
        return self.is_element_displayed(Locators.BURGER_MENU)

    def is_sort_container_displayed(self):
        """Verifica si el selector de ordenamiento está visible."""
        return self.is_element_displayed(Locators.SORT_CONTAINER)

    def is_cart_link_displayed(self):
        """Verifica si el ícono del carrito está visible."""
        return self.is_element_displayed(Locators.CART_LINK)
