from typing import Optional, cast

from typing_extensions import override

from pipelex import log
from pipelex.core.pipe import PipeAbstract
from pipelex.core.pipe_output import PipeOutputType
from pipelex.core.pipe_run_params import PipeRunParams
from pipelex.core.working_memory import WorkingMemory
from pipelex.hub import get_required_pipe
from pipelex.job_metadata import JobMetadata
from pipelex.pipe_works.pipe_router_job_factory import PipeRouterJobFactory
from pipelex.pipe_works.pipe_router_protocol import PipeRouterJob, PipeRouterProtocol


class PipeRouter(PipeRouterProtocol):
    @override
    async def run_pipe_router_workflow(
        self,
        pipe_router_job: PipeRouterJob,
        wfid: Optional[str] = None,
    ) -> PipeOutputType:  # pyright: ignore[reportInvalidTypeVarUse]
        log.debug("PipeRouterSimple run_pipe_router_workflow")
        working_memory = pipe_router_job.working_memory

        pipe = pipe_router_job.pipe
        log.verbose(f"Routing {pipe.__class__.__name__} pipe '{pipe_router_job.pipe.code}': {pipe.definition}")

        pipe_output = await pipe.run_pipe(
            pipe_code=pipe_router_job.pipe.code,
            job_metadata=pipe_router_job.job_metadata,
            working_memory=working_memory,
            output_name=pipe_router_job.output_name,
            pipe_run_params=pipe_router_job.pipe_run_params,
        )

        log.debug("Workflow complete")
        return cast(PipeOutputType, pipe_output)

    @override
    async def run_pipe_direct(
        self,
        pipe: PipeAbstract,
        pipe_run_params: Optional[PipeRunParams] = None,
        job_metadata: Optional[JobMetadata] = None,
        working_memory: Optional[WorkingMemory] = None,
        output_name: Optional[str] = None,
        wfid: Optional[str] = None,
    ) -> PipeOutputType:  # pyright: ignore[reportInvalidTypeVarUse]
        pipe_router_job = PipeRouterJobFactory.make_pipe_router_job_from_pipe(
            pipe=pipe,
            pipe_run_params=pipe_run_params,
            job_metadata=job_metadata,
            working_memory=working_memory,
            output_name=output_name,
        )
        pipe_output: PipeOutputType = await self.run_pipe_router_workflow(
            pipe_router_job=pipe_router_job,
            wfid=wfid,
        )
        return pipe_output

    @override
    async def run_pipe(
        self,
        pipe_code: str,
        pipe_run_params: Optional[PipeRunParams] = None,
        job_metadata: Optional[JobMetadata] = None,
        working_memory: Optional[WorkingMemory] = None,
        output_name: Optional[str] = None,
        wfid: Optional[str] = None,
    ) -> PipeOutputType:  # pyright: ignore[reportInvalidTypeVarUse]
        log.debug(f"run_pipe_direct: output_name={output_name}")
        pipe = get_required_pipe(pipe_code)
        pipe_router_job = PipeRouterJobFactory.make_pipe_router_job_from_pipe(
            pipe=pipe,
            job_metadata=job_metadata,
            working_memory=working_memory,
            output_name=output_name,
            pipe_run_params=pipe_run_params,
        )
        pipe_output: PipeOutputType = await self.run_pipe_router_workflow(
            pipe_router_job=pipe_router_job,
            wfid=wfid,
        )
        return pipe_output
