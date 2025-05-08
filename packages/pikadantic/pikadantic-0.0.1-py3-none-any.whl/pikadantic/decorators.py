from functools import wraps
from typing import Callable, Optional, TypeVar

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import BasicProperties
from pydantic import BaseModel, ValidationError

from pikadantic.exceptions import PikadanticValidationError

R = TypeVar("R")

WrappedCallback = Callable[[BlockingChannel, str, BasicProperties, bytes], Optional[R]]


def validate_body(model: type[BaseModel], *, json: bool = True, raise_on_error: bool = True):
    """
    Decorator that validates a message body against a Pydantic model before calling the handler.

    Args:
        model (Type[BaseModel]): Pydantic model class used for validation.
        json (bool): If True, parses body as JSON. If False, uses raw data. Default is True.
        raise_on_error (bool): If True, raises PikadanticValidationError on failure. Otherwise, skips handler.
        Default is True.

    Returns:
        Callable: The decorated handler function.

    Raises:
        PikadanticValidationError: If validation fails and raise_on_error is True.
    """

    def decorator(func: WrappedCallback[R]) -> WrappedCallback[Optional[R]]:
        @wraps(func)
        def wrapper(
            channel: BlockingChannel,
            method: str,
            properties: BasicProperties,
            body: bytes,
        ) -> Optional[R]:
            try:
                if json:
                    model.model_validate_json(body)
                else:
                    model.model_validate(body)
            except ValidationError as e:
                if raise_on_error:
                    raise PikadanticValidationError(e) from e
                return None

            return func(channel, method, properties, body)

        return wrapper

    return decorator


__all__ = ["validate_body"]
