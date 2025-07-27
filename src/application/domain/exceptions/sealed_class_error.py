from src.application.domain.enums.status_code import StatusCode


class SealedClassError(TypeError):
    """Raised when attempting to inherit from a sealed class."""
    __slots__ = ['_status_code', '_message']

    def __init__(self, status_code: StatusCode, message: str):
        self._status_code = status_code
        self._message = message

    @property
    def status_code(self) -> StatusCode:
        return self._status_code

    @property
    def message(self) -> str:
        return self._message

    def __str__(self) -> str:
        return f'{self.status_code.value} - {self.message}'
