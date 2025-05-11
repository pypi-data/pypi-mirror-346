from abc import ABC, abstractmethod

from pydantic import BaseModel


class ImggEngineAbstract(ABC, BaseModel):
    @property
    @abstractmethod
    def desc(self) -> str:
        pass
