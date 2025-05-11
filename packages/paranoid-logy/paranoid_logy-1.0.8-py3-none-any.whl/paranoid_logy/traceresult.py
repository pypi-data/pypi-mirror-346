from dataclasses import dataclass


@dataclass
class TraceResult:
    success: str
    serviceResponse: dict

    def __init__(self, success):
        self.success = success
