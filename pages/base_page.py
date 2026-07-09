import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.config import TIMEOUT

logger = logging.getLogger(__name__)

class BasePage:
    """
    Clase base para todos los Page Objects. Contiene métodos comunes
    para interactuar con la interfaz de usuario usando esperas explícitas.
    """
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, locator, timeout=TIMEOUT):
        logger.debug(f"Esperando presencia de elemento: {locator}")
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator),
            message=f"Timeout: elemento {locator} no encontrado en {timeout}s."
        )

    def wait_for_element_clickable(self, locator, timeout=TIMEOUT):
        logger.debug(f"Esperando que el elemento sea clickeable: {locator}")
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator),
            message=f"Timeout: elemento {locator} no clickeable en {timeout}s."
        )

    def click(self, locator, timeout=TIMEOUT):
        element = self.wait_for_element_clickable(locator, timeout)
        logger.info(f"Haciendo clic en elemento: {locator}")
        element.click()

    def send_keys(self, locator, text, clear_first=True, timeout=TIMEOUT):
        element = self.wait_for_element_clickable(locator, timeout)
        if clear_first:
            element.clear()
            logger.debug(f"Campo limpiado en elemento: {locator}")
        logger.info(f"Enviando texto a {locator}: '{text}'")
        element.send_keys(text)

    def get_text(self, locator, timeout=TIMEOUT):
        element = self.wait_for_element(locator, timeout)
        text = element.text.strip()
        logger.debug(f"Texto obtenido de {locator}: '{text}'")
        return text

    def is_element_displayed(self, locator, timeout=TIMEOUT):
        try:
            element = self.wait_for_element(locator, timeout)
            displayed = element.is_displayed()
            logger.debug(f"Elemento {locator} visible: {displayed}")
            return displayed
        except Exception:
            logger.debug(f"Elemento {locator} no está visible.")
            return False

    def wait_for_url_contains(self, url_fragment, timeout=TIMEOUT):
        logger.debug(f"Esperando que la URL contenga: '{url_fragment}'")
        return WebDriverWait(self.driver, timeout).until(
            EC.url_contains(url_fragment),
            message=f"Timeout: URL no contiene '{url_fragment}' en {timeout}s."
        )
