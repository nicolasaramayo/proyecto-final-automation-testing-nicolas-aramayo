# =============================================================================
# conftest.py - Configuración global de Pytest
# =============================================================================
# Este archivo es reconocido automáticamente por Pytest.
# Contiene los fixtures compartidos entre todos los tests y hooks especiales.
# =============================================================================

import os
import logging
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Configuración del logger para conftest
logger = logging.getLogger(__name__)


# =============================================================================
# FIXTURE: driver
# =============================================================================
# Scope "function" garantiza que cada test tenga su propia instancia de Chrome,
# asegurando independencia total entre casos de prueba.
# =============================================================================
@pytest.fixture(scope="function")
def driver():
    """
    Fixture que inicializa y proporciona una instancia de Chrome WebDriver.
    
    - Descarga automáticamente el ChromeDriver compatible con webdriver-manager.
    - Configura el navegador con ventana de 1280x800.
    - Deshabilita las esperas implícitas (se usarán esperas explícitas).
    - Al finalizar cada test, cierra el navegador limpiamente.
    """
    logger.info("⚙️  Iniciando instancia de Chrome WebDriver...")

    # Opciones del navegador Chrome
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1280,800")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Descomenta la siguiente línea para ejecutar en modo headless (sin interfaz):
    # chrome_options.add_argument("--headless=new")

    # Ruta al ChromeDriver 148 descargado localmente (compatible con Chrome 148)
    import os
    chromedriver_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "drivers", "chromedriver-win32", "chromedriver.exe"
    )
    service = Service(executable_path=chromedriver_path)
    chrome_driver = webdriver.Chrome(service=service, options=chrome_options)

    # Deshabilitar espera implícita (usamos esperas explícitas en helpers.py)
    chrome_driver.implicitly_wait(0)

    logger.info("✅ Chrome WebDriver iniciado correctamente.")

    # Ceder el driver al test
    yield chrome_driver

    # Teardown: cerrar el navegador al finalizar el test
    logger.info("🔒 Cerrando instancia de Chrome WebDriver...")
    chrome_driver.quit()


# =============================================================================
# HOOK: pytest_runtest_makereport
# =============================================================================
# Este hook se ejecuta después de cada fase del test (setup, call, teardown).
# Si la fase "call" (ejecución del test) falla, se toma una captura de pantalla
# automáticamente y se guarda en reports/screenshots/.
# =============================================================================
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook de Pytest que captura una screenshot automáticamente cuando un test falla.
    
    La imagen se guarda en reports/screenshots/ con el nombre del test y la fecha/hora.
    """
    # Ejecutar el test y obtener el resultado
    outcome = yield
    report = outcome.get_result()

    # Solo actuar si la fase de ejecución ("call") falla
    if report.when == "call" and report.failed:
        # Intentar obtener el driver desde el fixture del test
        driver_fixture = item.funcargs.get("driver", None)
        if driver_fixture:
            # Crear directorio de screenshots si no existe
            screenshots_dir = os.path.join("reports", "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)

            # Nombre de archivo con timestamp para evitar sobreescrituras
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_test_name = item.name.replace("::", "_").replace("/", "_")
            screenshot_path = os.path.join(
                screenshots_dir, f"{safe_test_name}_{timestamp}.png"
            )

            # Tomar y guardar la screenshot
            driver_fixture.save_screenshot(screenshot_path)
            logger.warning(f"📸 Screenshot guardada en: {screenshot_path}")
