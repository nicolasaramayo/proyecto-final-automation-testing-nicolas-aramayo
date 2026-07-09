import logging
from pages.base_page import BasePage
from utils.config import Locators

logger = logging.getLogger(__name__)

class CartPage(BasePage):
    """
    Page Object para la página del Carrito de Compras.
    """
    def get_cart_item_count(self):
        """Retorna el número de elementos en el carrito."""
        if self.is_element_displayed(Locators.CART_ITEMS, timeout=3):
            items = self.driver.find_elements(*Locators.CART_ITEMS)
            return len(items)
        return 0

    def get_cart_item_names(self):
        """Retorna una lista con los nombres de todos los productos en el carrito."""
        if not self.is_element_displayed(Locators.CART_ITEMS, timeout=3):
            return []
        items = self.driver.find_elements(*Locators.CART_ITEMS)
        names = []
        for item in items:
            try:
                name_element = item.find_element(*Locators.CART_ITEM_NAME)
                names.append(name_element.text.strip())
            except Exception as e:
                logger.warning(f"Error al obtener el nombre del producto en el carrito: {e}")
        return names

    def click_checkout(self):
        """Hace clic en el botón 'Checkout' para iniciar el proceso de pago."""
        self.click(Locators.CHECKOUT_BUTTON)
        logger.info("Navegando a la página de Checkout.")
