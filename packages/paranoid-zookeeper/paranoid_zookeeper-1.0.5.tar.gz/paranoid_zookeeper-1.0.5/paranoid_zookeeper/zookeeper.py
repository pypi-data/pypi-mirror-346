import json
import requests

from paranoid_zookeeper import Artifact, CheckInResult, ZookeeperServiceContext


class Zookeeper:

    __context: ZookeeperServiceContext = None

    def __init__(self, context: ZookeeperServiceContext):
        self.__context = context

    def check_in(self, art: Artifact):
        result = CheckInResult(True)
        try:
            endpoint = '{0}/{1}'.format(self.__context.base_endpoint, 'artifacts')
            response = requests.post(endpoint, json=art.as_json_without_nulls())
            if response.status_code != 200:
                result.success = False
                result.serviceResponse = {
                    'httpStatusCode': response.status_code,
                    'content': json.loads(response.content)
                }
                return result
            result.serviceResponse = {
                'httpStatusCode': 200,
                'content': ''
            }
        except Exception as ex:
            result.success = False
            result.serviceResponse = {
                'httpStatusCode': 500,
                'content': ex
            }
        return result

    @staticmethod
    def extract_dependencies(app_context_as_json_string):
        dependencies = []
        app_context_as_dict = json.loads(app_context_as_json_string)
        for key, value in app_context_as_dict.items():
            if not type(value) is dict:
                continue
            if not key.endswith('_context') and not key.endswith('Context'):
                continue
            if 'id' not in value.keys():
                continue
            dependencies.append(value['id'])
        return dependencies
