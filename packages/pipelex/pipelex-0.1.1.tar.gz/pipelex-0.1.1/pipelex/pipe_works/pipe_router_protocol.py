from typing import Optional, Protocol

from pipelex.core.pipe import PipeAbstract
from pipelex.core.pipe_output import PipeOutputType
from pipelex.core.pipe_run_params import PipeRunParams
from pipelex.core.working_memory import WorkingMemory
from pipelex.job_metadata import JobMetadata
from pipelex.pipe_works.pipe_router_job import PipeRouterJob


class PipeRouterProtocol(Protocol):
    async def run_pipe_router_workflow(
        self,
        pipe_router_job: PipeRouterJob,
        wfid: Optional[str] = None,
    ) -> PipeOutputType: ...  # pyright: ignore[reportInvalidTypeVarUse]

    async def run_pipe_direct(
        self,
        pipe: PipeAbstract,
        pipe_run_params: Optional[PipeRunParams] = None,
        job_metadata: Optional[JobMetadata] = None,
        working_memory: Optional[WorkingMemory] = None,
        output_name: Optional[str] = None,
        wfid: Optional[str] = None,
    ) -> PipeOutputType: ...  # pyright: ignore[reportInvalidTypeVarUse]

    async def run_pipe(
        self,
        pipe_code: str,
        pipe_run_params: Optional[PipeRunParams] = None,
        job_metadata: Optional[JobMetadata] = None,
        working_memory: Optional[WorkingMemory] = None,
        output_name: Optional[str] = None,
        wfid: Optional[str] = None,
    ) -> PipeOutputType: ...  # pyright: ignore[reportInvalidTypeVarUse]
