from abc import ABC
from typing import Any
from src.application.domain.exceptions import SealedClassError


class Sealed(ABC):
    """
    Base class for sealed objects.

    Once a class is defined as sealed, it prevents further inheritance. Any subclass
    attempt will raise an exception, ensuring that the class hierarchy remains fixed.
    """
    _is_sealed = False

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """
        Ensures that if the parent class is marked as sealed, any subclass attempt
        will raise an exception.

        Raises:
            SealedClassError: If an attempt is made to inherit from a sealed class.
        """
        super().__init_subclass__(**kwargs)
        for base in cls.__bases__:
            if hasattr(base, '_is_sealed') and getattr(base, '_is_sealed', False):
                raise SealedClassError(f"The class '{base.__name__}' cannot be inherited since it is sealed")

        cls._is_sealed = True
