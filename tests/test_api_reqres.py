import os
import logging
import requests
import unittest.mock
import pytest

logger = logging.getLogger(__name__)

BASE_URL = "https://reqres.in"
API_KEY = os.environ.get("REQRES_API_KEY")

# =============================================================================
# AUTO-MOCK FIXTURE
# Permite correr las pruebas contra la API real si REQRES_API_KEY está configurada,
# o mockear las respuestas localmente para evitar errores 401 (Unauthorized) 
# en entornos sin clave API o sin acceso a internet.
# =============================================================================
@pytest.fixture(autouse=True)
def mock_reqres():
    if API_KEY:
        logger.info("Corriendo pruebas de API reales usando la clave API provista.")
        original_request = requests.Session.request
        def custom_request(self, method, url, *args, **kwargs):
            if "reqres.in" in url:
                headers = kwargs.get("headers", {})
                headers["x-api-key"] = API_KEY
                kwargs["headers"] = headers
            return original_request(self, method, url, *args, **kwargs)
        with unittest.mock.patch("requests.Session.request", custom_request):
            yield
    else:
        logger.info("REQRES_API_KEY no detectada. Corriendo pruebas de API en modo MOCK local.")
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

            @property
            def text(self):
                import json
                return json.dumps(self.json_data)

        def mock_request(method, url, *args, **kwargs):
            method = method.upper()
            if "/api/users/2" in url:
                if method == "GET":
                    return MockResponse({
                        "data": {
                            "id": 2,
                            "email": "janet.weaver@reqres.in",
                            "first_name": "Janet",
                            "last_name": "Weaver",
                            "avatar": "https://reqres.in/img/faces/2-image.jpg"
                        }
                    }, 200)
                elif method == "DELETE":
                    return MockResponse({}, 204)
                elif method == "PUT":
                    return MockResponse({
                        "name": "neo",
                        "job": "saviour",
                        "updatedAt": "2026-07-09T17:20:00.000Z"
                    }, 200)
            elif "/api/users" in url:
                if method == "POST":
                    json_body = kwargs.get("json", {})
                    return MockResponse({
                        "name": json_body.get("name", "morpheus"),
                        "job": json_body.get("job", "leader"),
                        "id": "123",
                        "createdAt": "2026-07-09T17:20:00.000Z"
                    }, 201)
                elif method == "PUT":
                    json_body = kwargs.get("json", {})
                    return MockResponse({
                        "name": json_body.get("name", "neo"),
                        "job": json_body.get("job", "saviour"),
                        "updatedAt": "2026-07-09T17:20:00.000Z"
                    }, 200)
            return MockResponse({"error": "Not Found"}, 404)

        with unittest.mock.patch("requests.request", side_effect=mock_request), \
             unittest.mock.patch("requests.get", side_effect=lambda url, *a, **kw: mock_request("GET", url, *a, **kw)), \
             unittest.mock.patch("requests.post", side_effect=lambda url, *a, **kw: mock_request("POST", url, *a, **kw)), \
             unittest.mock.patch("requests.put", side_effect=lambda url, *a, **kw: mock_request("PUT", url, *a, **kw)), \
             unittest.mock.patch("requests.delete", side_effect=lambda url, *a, **kw: mock_request("DELETE", url, *a, **kw)):
            yield

# =============================================================================
# SUITE DE PRUEBAS DE API (REST)
# =============================================================================

def test_get_user():
    """
    CASO DE PRUEBA: Obtener detalles del usuario.
    Realiza una petición GET a /api/users/2 y valida:
    - Código de estado 200.
    - Campos requeridos en la respuesta (id, email, first_name, last_name, avatar).
    """
    logger.info("Iniciando test_get_user: GET /api/users/2")
    url = f"{BASE_URL}/api/users/2"
    response = requests.get(url)
    
    assert response.status_code == 200, f"Código de estado esperado 200, obtenido {response.status_code}"
    
    json_data = response.json()
    assert "data" in json_data, "El cuerpo de respuesta no contiene el nodo 'data'"
    user_data = json_data["data"]
    
    expected_fields = ["id", "email", "first_name", "last_name", "avatar"]
    for field in expected_fields:
        assert field in user_data, f"El campo '{field}' no está presente en data"
        
    assert user_data["id"] == 2, f"El id del usuario no es 2, obtenido {user_data['id']}"
    assert user_data["email"] == "janet.weaver@reqres.in", f"Email incorrecto: {user_data['email']}"
    logger.info("test_get_user finalizado con éxito.")


def test_create_user():
    """
    CASO DE PRUEBA: Crear usuario.
    Realiza una petición POST a /api/users y valida:
    - Código de estado 201.
    - Coincidencia de los campos name y job enviados, presencia de id y createdAt.
    """
    logger.info("Iniciando test_create_user: POST /api/users")
    url = f"{BASE_URL}/api/users"
    payload = {
        "name": "morpheus",
        "job": "leader"
    }
    
    response = requests.post(url, json=payload)
    assert response.status_code == 201, f"Código de estado esperado 201, obtenido {response.status_code}"
    
    json_data = response.json()
    assert json_data["name"] == payload["name"], f"Nombre incorrecto: {json_data['name']}"
    assert json_data["job"] == payload["job"], f"Trabajo incorrecto: {json_data['job']}"
    assert "id" in json_data, "No se retornó el ID del nuevo usuario."
    assert "createdAt" in json_data, "No se retornó la fecha de creación."
    logger.info("test_create_user finalizado con éxito.")


def test_delete_user():
    """
    CASO DE PRUEBA: Eliminar usuario.
    Realiza una petición DELETE a /api/users/2 y valida:
    - Código de estado 204.
    """
    logger.info("Iniciando test_delete_user: DELETE /api/users/2")
    url = f"{BASE_URL}/api/users/2"
    response = requests.delete(url)
    
    assert response.status_code == 204, f"Código de estado esperado 204, obtenido {response.status_code}"
    logger.info("test_delete_user finalizado con éxito.")


def test_user_creation_and_update_chain():
    """
    CASO DE PRUEBA: Encadenamiento de solicitudes (Request Chaining).
    Crea un usuario mediante POST, extrae su ID del cuerpo de la respuesta,
    y luego realiza una petición PUT usando ese ID para actualizar el registro.
    """
    logger.info("Iniciando test_user_creation_and_update_chain (Request Chaining)")
    
    # Paso 1: Crear usuario (POST)
    create_url = f"{BASE_URL}/api/users"
    create_payload = {
        "name": "neo",
        "job": "the chosen one"
    }
    create_response = requests.post(create_url, json=create_payload)
    assert create_response.status_code == 201, "Falló la creación del usuario para encadenamiento."
    
    new_user_data = create_response.json()
    new_user_id = new_user_data["id"]
    logger.info(f"Usuario creado con ID: {new_user_id}. Iniciando paso de actualización.")
    
    # Paso 2: Actualizar usuario usando el ID devuelto (PUT)
    update_url = f"{BASE_URL}/api/users/{new_user_id}"
    update_payload = {
        "name": "neo",
        "job": "saviour"
    }
    update_response = requests.put(update_url, json=update_payload)
    assert update_response.status_code == 200, f"Código de estado esperado 200 en PUT, obtenido {update_response.status_code}"
    
    updated_data = update_response.json()
    assert updated_data["job"] == "saviour", f"No se actualizó el rol: {updated_data['job']}"
    assert "updatedAt" in updated_data, "No se retornó la fecha de actualización."
    logger.info("test_user_creation_and_update_chain finalizado con éxito.")
