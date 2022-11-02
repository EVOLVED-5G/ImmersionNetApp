from enum import Enum


class ActionResult(str, Enum):
    SUCCESS = "toastSuccess",
    WARNING = "toastWarning",
    ERROR = "toastError"

