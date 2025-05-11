from dataclasses import dataclass


@dataclass
class HttpHealthCheck:
    url: str
    portNumber: int

    def __init__(self, url: str, port_number: int):
        self.url = url
        self.portNumber = port_number
