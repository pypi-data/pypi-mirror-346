from abc import ABC

from pydantic import BaseModel
from typing_extensions import override


class PromptImage(BaseModel, ABC):
    pass


class PromptImagePath(PromptImage):
    file_path: str

    @override
    def __str__(self) -> str:
        return f"PromptImagePath(file_path='{self.file_path}')"


class PromptImageUrl(PromptImage):
    # image_format: str = "jpeg"
    url: str

    @override
    def __str__(self) -> str:
        return f"PromptImageUrl(url='{self.url}')"


class PromptImageBytes(PromptImage):
    # image_format: str = "jpeg"
    image_bytes: bytes

    @override
    def __str__(self) -> str:
        bytes_sample: str = str(self.image_bytes[:20])
        if len(self.image_bytes) > 20:
            bytes_sample += "..."
        bytes_preview = f"{len(self.image_bytes)} bytes: {bytes_sample}"
        return f"PromptImageBytes(image_bytes={bytes_preview})"

    @override
    def __repr__(self) -> str:
        return self.__str__()
