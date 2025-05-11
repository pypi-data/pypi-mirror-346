from enum import StrEnum


class PipeJobMacroTask(StrEnum):
    PIPE_LLM = "pipe_llm"
    PIPE_IMGG = "pipe_imgg"
    PIPE_LMM_PROMPT = "pipe_lmm_prompt"
    PIPE_SCRIPT = "pipe_script"
