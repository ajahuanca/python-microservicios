import os
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential_jitter, retry_if_exception_type
import pybreaker
import logging


logger = logging.getLogger(__name__)


# Circuit Breaker configuration
breaker = pybreaker.CircuitBreaker(fail_max=4, reset_timeout=20)


SERVICE_A_URL = os.getenv('SERVICE_A_URL', 'http://service_empresas:8000')
SERVICE_C_URL = os.getenv('SERVICE_C_URL', 'http://service_programacion:8000')


@retry(stop=stop_after_attempt(3), wait=wait_exponential_jitter(1, 5),
       retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)))
@breaker
def call_service(url_path: str):
    url = url_path
    try:
        with httpx.Client(timeout=5.0) as client:
            r = client.get(url)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        logger.exception("Error calling %s: %s", url, e)
        raise


def get_empresa(empresa_id: int):
    return call_service(f"{SERVICE_A_URL}/empresas/{empresa_id}/")


def get_programacion(proyecto_id: int):
    return call_service(f"{SERVICE_C_URL}/programacion/{proyecto_id}/")
