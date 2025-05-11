from typing import Optional

from typing_extensions import override

from pipelex.cogt.ocr.ocr_engine_abstract import OCREngineAbstract
from pipelex.cogt.ocr.ocr_engine_factory import OCREngineFactory
from pipelex.core.pipe import PipeAbstract, update_job_metadata_for_pipe
from pipelex.core.pipe_output import PipeOutput
from pipelex.core.pipe_run_params import PipeRunParams
from pipelex.core.stuff_content import TextContent
from pipelex.core.stuff_factory import StuffFactory
from pipelex.core.working_memory import WorkingMemory
from pipelex.job_metadata import JobMetadata
from pipelex.tools.utils.path_utils import clarify_path_or_url


class PipeOCROutput(PipeOutput):
    pass


class PipeOCR(PipeAbstract):
    image: str
    ocr_model_name: str

    @override
    @update_job_metadata_for_pipe
    async def run_pipe(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        pipe_code: str,
        job_metadata: JobMetadata,
        working_memory: WorkingMemory,
        pipe_run_params: PipeRunParams,
        output_name: Optional[str] = None,
    ) -> PipeOCROutput:
        if not self.output_concept_code:
            raise ValueError("PipeOCR should have a non-None output_concept_code")
        image_stuff = working_memory.get_stuff(name=self.image)
        image_url = image_stuff.as_image.url

        image_path, url = clarify_path_or_url(path_or_url=image_url)  # pyright: ignore
        if not image_stuff.is_image:
            raise ValueError(f"Image stuff '{self.image}' is not an image")

        ocr_engine: OCREngineAbstract = OCREngineFactory.make_ocr_engine(
            self.ocr_model_name,
        )

        ocr_output = await ocr_engine.extract_text_from_image(
            image_path=image_path,
            image_url=url,
        )

        ocr_output_text = ocr_output.text

        output_stuff = StuffFactory.make_stuff(
            name=output_name,
            concept_code=self.output_concept_code,
            content=TextContent(text=ocr_output_text),
        )

        working_memory.set_new_main_stuff(
            stuff=output_stuff,
            name=output_name,
        )

        pipe_output = PipeOCROutput(
            working_memory=working_memory,
        )
        return pipe_output
