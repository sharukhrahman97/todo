from pydantic import BaseModel
from typing import Optional, Generic, TypeVar
from pydantic.generics import GenericModel

T = TypeVar("T")


class StandardResponse(GenericModel, Generic[T]):
    status: int
    message: str
    data: Optional[T] = None

class ErrorResponse(BaseModel):
    status: int
    message: str
    error: Optional[dict] = None
