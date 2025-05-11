from typing import Any, Callable

from pydantic import BaseModel


class ActivityReport(BaseModel):
    content: Any


ActivityCallback = Callable[[ActivityReport], None]
