from pipelex.tools.exceptions import FatalError, RootException


class ConfigValidationError(FatalError):
    pass


class ConfigNotFoundError(RootException):
    pass


class LLMPresetNotFoundError(ConfigNotFoundError):
    pass


class LLMSettingsValidationError(ConfigValidationError):
    pass


class LLMDeckValidatonError(ConfigValidationError):
    pass


class LLMHandleNotFoundError(ConfigNotFoundError):
    pass


class ConfigModelError(ValueError, FatalError):
    pass
