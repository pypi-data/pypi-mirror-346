from dataclasses import dataclass


@dataclass
class ZookeeperServiceContext:

    id: str
    base_endpoint: str
    headers: dict

    def __init__(self, settings):
        self.id = settings['id']
        self.base_endpoint = settings['baseEndpoint']
        self.headers = settings['headers']
