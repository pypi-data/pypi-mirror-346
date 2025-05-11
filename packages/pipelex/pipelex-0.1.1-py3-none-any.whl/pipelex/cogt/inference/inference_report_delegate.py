from typing import Protocol

from pipelex.cogt.inference.inference_job_abstract import InferenceJobAbstract


class InferenceReportDelegate(Protocol):
    def report_inference_job(self, inference_job: InferenceJobAbstract): ...

    def general_report(self): ...
