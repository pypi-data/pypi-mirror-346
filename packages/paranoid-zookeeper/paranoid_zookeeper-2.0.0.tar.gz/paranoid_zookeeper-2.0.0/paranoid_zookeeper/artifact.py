import dataclasses
from dataclasses import dataclass
from paranoid_zookeeper.httphealthcheck import HttpHealthCheck


def enum(**enums):
    return type('Enum', (), enums)


ArtifactTypeEnum = enum(
    Api='Api',
    WebApplication='WebApplication',
    Service='Service',
    Daemon='Daemon',
    Database='Database',
    LoadBalancer='LoadBalancer',
    Proxy='Proxy',
    Server='Service'
)


@dataclass
class Artifact:
    id: str
    name: str
    description: str
    ipAddress: str
    httpHealthCheck: HttpHealthCheck
    type: ArtifactTypeEnum
    dependsOn: [str]
    tags: [str]

    def __init__(self, id: str, name: str, description: str, id_address: str, http_health_check: HttpHealthCheck, type: ArtifactTypeEnum, depends_on=[str], tags=[]):
        self.id = id
        self.name = name
        self.description = description
        self.ipAddress = id_address
        self.httpHealthCheck = http_health_check
        self.type = type
        self.dependsOn = depends_on
        self.tags = tags

    def as_json_without_nulls(self):
        return {key: value for key, value in dataclasses.asdict(self).items() if value is not None}

