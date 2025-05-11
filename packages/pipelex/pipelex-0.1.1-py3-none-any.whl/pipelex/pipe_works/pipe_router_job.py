from typing import Optional

from pydantic import BaseModel, Field

from pipelex.core.pipe import PipeAbstract
from pipelex.core.pipe_run_params import PipeRunParams
from pipelex.core.working_memory import WorkingMemory
from pipelex.job_metadata import JobMetadata


class PipeRouterJob(BaseModel):
    job_metadata: JobMetadata
    working_memory: WorkingMemory = Field(default_factory=WorkingMemory)
    pipe: PipeAbstract
    output_name: Optional[str] = None
    pipe_run_params: PipeRunParams
