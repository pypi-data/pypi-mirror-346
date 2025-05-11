from typing import Optional

from pipelex import pretty_print
from pipelex.config import get_config
from pipelex.core.pipe_output import PipeOutput
from pipelex.core.pipe_run_params import PipeOutputMultiplicity, PipeRunParams
from pipelex.core.working_memory import WorkingMemory
from pipelex.core.working_memory_factory import WorkingMemoryFactory
from pipelex.hub import get_pipe_router, get_required_pipe
from pipelex.job_metadata import JobMetadata
from pipelex.pipe_works.pipe_router_job import PipeRouterJob


async def execute_pipe(
    pipe_code: str,
    working_memory: Optional[WorkingMemory] = None,
    output_multiplicity: Optional[PipeOutputMultiplicity] = None,
    output_concept_code: Optional[str] = None,
    job_id: Optional[str] = None,
) -> PipeOutput:
    """
    Simple wrapper to run a pipe with a working memory using a PipeRouter.

    Args:
        pipe_code: The code of the pipe to run
        working_memory: The working memory containing all necessary stuffs
        output_multiplicity: The multiplicity of the output
        output_concept_code: Optional output concept code
        job_id: Optional job ID (defaults to pipe_code)

    Returns:
        PipeOutput: The output of the pipe execution
    """
    pipe = get_required_pipe(pipe_code=pipe_code)

    job_metadata = JobMetadata(
        session_id=get_config().session_id,
        top_job_id=job_id or pipe_code,
    )

    pipe_run_params = PipeRunParams(
        output_multiplicity=output_multiplicity,
        output_concept_code=output_concept_code,
    )

    pretty_print(pipe, title=f"Running pipe '{pipe_code}'")
    if working_memory:
        working_memory.pretty_print_summary()

    pipe_router_job = PipeRouterJob(
        pipe=pipe,
        job_metadata=job_metadata,
        working_memory=working_memory or WorkingMemoryFactory.make_empty(),
        pipe_run_params=pipe_run_params,
    )

    return await get_pipe_router().run_pipe_router_workflow(pipe_router_job)
