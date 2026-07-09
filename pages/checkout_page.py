import logging
from pages.base_page import BasePage
from utils.config import Locators

logger = logging.getLogger(__name__)

class CheckoutPage(BasePage):
    """
    Page Object para los pasos del Checkout (información del cliente, vista previa y confirmación).
    """
    def fill_client_details(self, first_name, last_name, postal_code):
        """Llena los campos de información personal del cliente."""
        self.send_keys(Locators.FIRST_NAME_INPUT, first_name)
        self.send_keys(Locators.LAST_NAME_INPUT, last_name)
        self.send_keys(Locators.POSTAL_CODE_INPUT, postal_code)
        logger.info(f"Datos del cliente completados: {first_name} {last_name}, CP: {postal_code}")

    def click_continue(self):
        """Hace clic en el boton 'Continue' para pasar al siguiente paso."""
        btn = self.wait_for_element_clickable(Locators.CONTINUE_BUTTON)
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait_for_url_contains("/checkout-step-two.html")
        logger.info("Clic en 'Continue' de Checkout.")

    def click_finish(self):
        """Hace clic en el boton 'Finish' para completar la compra."""
        btn = self.wait_for_element_clickable(Locators.FINISH_BUTTON)
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait_for_url_contains("/checkout-complete.html")
        logger.info("Clic en 'Finish' para completar el pedido.")

    def get_complete_header_text(self):
        """Retorna el texto del encabezado final cuando la compra es exitosa."""
        return self.get_text(Locators.COMPLETE_HEADER)
