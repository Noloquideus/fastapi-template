import asyncio
import functools
from typing import Callable, Any, Awaitable
from src.infrastructure.logger import Logger, logger


def retry(
    retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
):
    """
    Decorator for retrying an async function on any exception.
    :param retries: Number of retries.
    :param delay: Initial delay between retries (in seconds).
    :param backoff: Multiplier to increase the delay after each failed retries.
    """

    def decorator(func: Callable[..., Awaitable[Any]]):

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            current_delay = delay
            __logger: Logger = logger

            func_name = getattr(func, '__qualname__', getattr(func, '__name__', 'unknown_function'))

            for attempt in range(1, retries + 1):
                try:
                    __logger.debug(f'Attempting {attempt} execution {func_name}')
                    return await func(*args, **kwargs)
                except Exception as e:
                    __logger.debug(
                        f'Error in {func_name}: {e} '
                        f'(attempt {attempt} of {retries}). Retry in {current_delay:.1f} sec'
                    )
                    if attempt == retries:
                        __logger.debug(f'All attempts for {func_name} exhausted.')
                        raise
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff

        return wrapper

    return decorator
