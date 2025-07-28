from src.application.domain.enums.status_code import StatusCode
from src.application.domain.objects.immutable import Immutable
from src.application.domain.objects.incomparable import Incomparable


class ApplicationException(Exception, Incomparable, Immutable):
    """Base class for application exceptions"""
    __slots__ = ['_status_code', '_message']

    def __init__(self, status_code: StatusCode, message: str) -> None:
        self._status_code: StatusCode = status_code
        self._message: str = message

    @property
    def status_code(self) -> StatusCode:
        return self._status_code

    @property
    def message(self) -> str:
        return self._message

    def __str__(self) -> str:
        return f'{self.status_code.value} - {self.message}'
