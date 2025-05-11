from typing import Optional

from pipelex.config import get_config
from pipelex.core.pipe import PipeAbstract
from pipelex.core.pipe_run_params import PipeRunParams
from pipelex.core.working_memory import WorkingMemory
from pipelex.job_metadata import JobMetadata
from pipelex.pipe_works.pipe_router_job import PipeRouterJob


class PipeRouterJobFactory:
    @classmethod
    def make_pipe_router_job_from_pipe(
        cls,
        pipe: PipeAbstract,
        pipe_run_params: Optional[PipeRunParams] = None,
        job_metadata: Optional[JobMetadata] = None,
        working_memory: Optional[WorkingMemory] = None,
        output_name: Optional[str] = None,
    ) -> PipeRouterJob:
        job_metadata = job_metadata or JobMetadata(session_id=get_config().session_id)
        working_memory = working_memory or WorkingMemory()
        if not pipe_run_params:
            pipe_run_params = PipeRunParams()
        return PipeRouterJob(
            job_metadata=job_metadata,
            working_memory=working_memory,
            pipe=pipe,
            output_name=output_name,
            pipe_run_params=pipe_run_params,
        )
