from dataclasses import dataclass


@dataclass
class CheckInResult:
    success: str
    serviceResponse: dict

    def __init__(self, success):
        self.success = success
