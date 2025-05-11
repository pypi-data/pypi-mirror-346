import asyncio
from typing import Annotated, Any, Dict, List, Optional

import pandas as pd
import typer
from pydantic import BaseModel

from pipelex import log, pretty_print
from pipelex.config import get_config
from pipelex.core.pipe_output import PipeOutput
from pipelex.core.pipe_run_params import PipeRunParams
from pipelex.core.stuff_content import StructuredContent
from pipelex.core.stuff_factory import StuffBlueprint, StuffFactory
from pipelex.core.working_memory_factory import WorkingMemoryFactory
from pipelex.hub import get_pipe_router
from pipelex.job_metadata import JobMetadata
from pipelex.tools.utils.file_utils import load_from_path

app = typer.Typer()


class FeatureSheet(BaseModel):
    pipe_code: str
    input_name: str
    output_name: str
    input_concept_code: str


# TODO: load this from a config file
PIPE_FEATURES: Dict[str, FeatureSheet] = {
    "transcript-gantt-chart": FeatureSheet(
        pipe_code="extract_gantt_by_steps",
        input_name="gantt_chart",
        output_name="gantt_chart_transcript",
        input_concept_code="GanttChart",
    ),
    "contract-fields": FeatureSheet(
        pipe_code="enrich_question",
        input_name="question",
        output_name="question_enrichment",
        input_concept_code="answer.Question",
    ),
}


async def run_feature_single(
    pipe_feature_code: str,
    input_value: str,
) -> PipeOutput:
    pipe_feature = PIPE_FEATURES[pipe_feature_code]
    pipe_code = pipe_feature.pipe_code

    blueprint = StuffBlueprint(
        name=pipe_feature.input_name,
        concept=pipe_feature.input_concept_code,
        value=input_value,
    )
    log.debug(f"Running pipe '{pipe_code}', using top_run_pipe")
    pretty_print(blueprint, title="blueprint")
    stuff_from_blueprint = StuffFactory.make_from_blueprint(blueprint=blueprint)
    working_memory = WorkingMemoryFactory.make_from_single_stuff(stuff=stuff_from_blueprint)

    pipe_output: PipeOutput = await get_pipe_router().run_pipe(
        pipe_code=pipe_code,
        pipe_run_params=PipeRunParams(),
        job_metadata=JobMetadata(
            session_id=get_config().session_id,
            top_job_id=pipe_feature_code,
        ),
        working_memory=working_memory,
        output_name=pipe_feature.output_name,
    )
    return pipe_output


async def _pipe_single_item(
    item: str,
    pipe_feature: FeatureSheet,
    project_context: Optional[str] = None,
) -> PipeOutput:
    blueprint = StuffBlueprint(
        name=pipe_feature.input_name,
        concept=pipe_feature.input_concept_code,
        value=item,
    )
    pipe_code = pipe_feature.pipe_code
    log.debug(f"Running pipe {pipe_code}, with input blueprint {blueprint}")
    stuff_from_blueprint = StuffFactory.make_from_blueprint(blueprint=blueprint)
    working_memory = WorkingMemoryFactory.make_from_single_stuff(stuff=stuff_from_blueprint)

    if project_context:
        project_context_stuff = StuffFactory.make_from_str(
            concept_code="questions.ProjectContext",
            str_value=project_context,
            name="project_context",
        )
        working_memory.set_stuff(
            name="project_context",
            stuff=project_context_stuff,
        )

    pipe_output: PipeOutput = await get_pipe_router().run_pipe(
        pipe_code=pipe_code,
        pipe_run_params=PipeRunParams(),
        job_metadata=JobMetadata(
            session_id=get_config().session_id,
            top_job_id=item,
        ),
        working_memory=working_memory,
        output_name=pipe_feature.output_name,
    )
    return pipe_output


async def _process_single_item(
    item: str,
    pipe_feature: FeatureSheet,
    project_context: Optional[str] = None,
) -> Dict[str, Any]:
    pipe_output = await _pipe_single_item(
        item=item,
        pipe_feature=pipe_feature,
        project_context=project_context,
    )
    return {"item": item, **pipe_output.main_stuff_as(content_type=StructuredContent).smart_dump()}


async def run_feature_spreadsheet(
    pipe_feature_code: str,
    items: List[str],
    project_context_file_path: Optional[str] = None,
    output_file_path: Annotated[Optional[str], typer.Option(help="Output filename")] = None,
):
    project_context: Optional[str] = None
    if project_context_file_path:
        project_context = load_from_path(project_context_file_path)
    else:
        project_context = None

    pipe_feature = PIPE_FEATURES[pipe_feature_code]
    # Process items concurrently using asyncio.gather
    stuff_dicts = await asyncio.gather(
        *[
            _process_single_item(
                item=item,
                pipe_feature=pipe_feature,
                project_context=project_context,
            )
            for item in items
        ]
    )

    df = pd.DataFrame(stuff_dicts)

    df.to_excel(  # pyright: ignore[reportUnknownMemberType]
        output_file_path,
        index=False,
        freeze_panes=(1, 0),
    )
