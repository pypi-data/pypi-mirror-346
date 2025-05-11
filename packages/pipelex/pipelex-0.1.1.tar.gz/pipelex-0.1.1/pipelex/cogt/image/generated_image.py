from pydantic import BaseModel


class GeneratedImage(BaseModel):
    # image_format: str = "jpeg"
    url: str
    width: int
    height: int
