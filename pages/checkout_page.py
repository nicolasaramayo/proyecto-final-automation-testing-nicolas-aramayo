import logging
from pages.base_page import BasePage
from utils.config import Locators

logger = logging.getLogger(__name__)

class CheckoutPage(BasePage):
    """
    Page Object para los pasos del Checkout (información del cliente, vista previa y confirmación).
    """
    def fill_client_details(self, first_name, last_name, postal_code):
        """Llena los campos de informacion personal del cliente."""
        import time
        first_name_field = self.wait_for_element_clickable(Locators.FIRST_NAME_INPUT)
        first_name_field.clear()
        first_name_field.send_keys(first_name)
        time.sleep(0.3)
        
        last_name_field = self.wait_for_element_clickable(Locators.LAST_NAME_INPUT)
        last_name_field.clear()
        last_name_field.send_keys(last_name)
        time.sleep(0.3)
        
        postal_field = self.wait_for_element_clickable(Locators.POSTAL_CODE_INPUT)
        postal_field.clear()
        postal_field.send_keys(postal_code)
        time.sleep(0.3)
        
        logger.info(f"Datos del cliente completados: {first_name} {last_name}, CP: {postal_code}")

    def click_continue(self):
        """Envia el formulario de checkout usando submit() en el campo postal."""
        import time
        time.sleep(1)
        postal_field = self.wait_for_element_clickable(Locators.POSTAL_CODE_INPUT)
        postal_field.submit()
        logger.info("Formulario enviado via submit().")

    def click_finish(self):
        """Hace clic en el boton 'Finish' para completar la compra."""
        import time
        time.sleep(1)
        btn = self.wait_for_element_clickable(Locators.FINISH_BUTTON)
        self.driver.execute_script("arguments[0].click();", btn)
        logger.info("Clic en 'Finish' para completar el pedido.")

    def get_complete_header_text(self):
        """Retorna el texto del encabezado final cuando la compra es exitosa."""
        return self.get_text(Locators.COMPLETE_HEADER)
