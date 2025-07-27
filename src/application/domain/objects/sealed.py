from abc import ABC
from src.application.domain.exceptions import SealedClassError


class Sealed(ABC):
    """
    Base class for sealed objects.

    Once a class is defined as sealed, it prevents further inheritance. Any subclass
    attempt will raise an exception, ensuring that the class hierarchy remains fixed.
    """
    _is_sealed = False

    def __init_subclass__(cls, **kwargs):
        """
        Ensures that if the parent class is marked as sealed, any subclass attempt
        will raise an exception.

        Raises:
            SealedClassError: If an attempt is made to inherit from a sealed class.
        """
        super().__init_subclass__(**kwargs)
        if cls.__bases__[0]._is_sealed:
            raise SealedClassError(f"The class '{cls.__bases__[0].__name__}' cannot be inherited since it is sealed")

        cls._is_sealed = True
