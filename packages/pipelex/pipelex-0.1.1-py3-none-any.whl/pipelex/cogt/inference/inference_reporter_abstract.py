from abc import ABC, abstractmethod
from typing import Optional

from pipelex.cogt.inference.inference_report_delegate import InferenceReportDelegate


class InferenceReporterAbstract(ABC):
    def __init__(
        self,
        report_delegate: Optional[InferenceReportDelegate] = None,
    ):
        self.report_delegate = report_delegate

    @property
    @abstractmethod
    def desc(self) -> str:
        pass
