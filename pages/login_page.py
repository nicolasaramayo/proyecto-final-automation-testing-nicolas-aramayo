from pages.base_page import BasePage
from utils.config import Locators, BASE_URL

class LoginPage(BasePage):
    """
    Page Object para la página de Login de SauceDemo.
    """
    def navigate(self):
        """Navega a la URL base de SauceDemo."""
        self.driver.get(BASE_URL)

    def login(self, username, password):
        """Realiza el flujo de login ingresando credenciales y haciendo clic."""
        self.send_keys(Locators.USERNAME_INPUT, username)
        self.send_keys(Locators.PASSWORD_INPUT, password)
        self.click(Locators.LOGIN_BUTTON)

    def get_error_message(self):
        """Retorna el texto del mensaje de error."""
        return self.get_text(Locators.ERROR_MESSAGE)

    def is_error_displayed(self):
        """Verifica si el mensaje de error está visible."""
        return self.is_element_displayed(Locators.ERROR_MESSAGE)
