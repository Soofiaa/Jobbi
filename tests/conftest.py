from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest


class FakeQuery:
    """Doble de prueba para el query builder fluido de postgrest-py.

    Cualquier método encadenable (select, insert, update, delete, eq, ilike,
    gte, lte, order, ...) se registra en `calls` y devuelve `self` para
    permitir el encadenado. `execute()` devuelve una respuesta con los
    datos configurados de antemano.
    """

    def __init__(self, data):
        self._data = data
        self.calls = []

    def __getattr__(self, name):
        def metodo(*args, **kwargs):
            self.calls.append((name, args, kwargs))
            return self
        return metodo

    def execute(self):
        return SimpleNamespace(data=self._data)

    def llamada(self, nombre):
        """Devuelve la primera llamada registrada con ese nombre, o None."""
        for call in self.calls:
            if call[0] == nombre:
                return call
        return None


@pytest.fixture
def fake_client(mocker):
    """Mockea get_client() en services.postulaciones (no requiere red ni .env).

    Uso: query = fake_client(data=[...]) -> configura la respuesta de execute()
    y devuelve el FakeQuery para inspeccionar qué se llamó.
    """
    def factory(data=None):
        query = FakeQuery(data if data is not None else [])
        client = MagicMock()
        client.table.return_value = query
        mocker.patch("services.postulaciones.get_client", return_value=client)
        return query
    return factory
