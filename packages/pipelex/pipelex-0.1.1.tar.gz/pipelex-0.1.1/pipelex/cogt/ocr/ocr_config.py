from pydantic import BaseModel


class MistralOCRConfig(BaseModel):
    ocr_model_name: str


class OCRConfig(BaseModel):
    mistral_ocr_config: MistralOCRConfig
