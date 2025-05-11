import json
import traceback
import requests

from paranoid_logy import LogyServiceContext, TraceResult


class Logy:

    __source: str
    __ip_address: str
    __context: LogyServiceContext = None

    def __init__(self, source: str, ip_address: str, context: LogyServiceContext):
        self.__source = source
        self.__ip_address = ip_address
        self.__context = context

    def trace_activity(self, message: str, additional_info=None, tags=None):
        result = TraceResult(True)
        payload = {
            'source': self.__source,
            'message': message,
            'ipAddress': self.__ip_address,
            'isException': False,
            'tags': tags if tags is not None else []
        }
        if additional_info is not None:
            payload['additionalInfo'] = additional_info
        try:
            response = requests.post(f'{self.__context.base_endpoint}/messages', headers=self.__context.headers, json=payload, timeout=0.75)
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
            return result
        except Exception as ex:
            result.success = False
            result.serviceResponse = {
                'httpStatusCode': 500,
                'content': ex
            }

        return result

    def trace_exception(self, ex: Exception, additional_info=None, tags=None):
        result = TraceResult(True)
        payload = {
            'source': self.__source,
            'message': str(ex),
            'ipAddress': self.__ip_address,
            'isException': True,
            'stackTrace': ''.join(traceback.format_tb(ex.__traceback__)),
            'tags': tags if tags is not None else []
        }
        if additional_info is not None:
            payload['additionalInfo'] = additional_info
        try:
            response = requests.post(f'{self.__context.base_endpoint}/messages', headers=self.__context.headers, json=payload)
            if response.status_code != 200:
                result.success = False
                result.serviceResponse = {
                    'httpStatusCode': response.status_code,
                    'content': json.loads(response.content)
                }
            result.serviceResponse = {
                'httpStatusCode': 200,
                'content': ''
            }
            return result
        except Exception as ex:
            result.success = False
            result.serviceResponse = {
                'httpStatusCode': 500,
                'content': ex
            }

        return result
