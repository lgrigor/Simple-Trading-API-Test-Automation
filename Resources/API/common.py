import json

import requests

from Data.main import Main


class Common(Main):

    @staticmethod
    def verify_status_code(response: requests.models.Response, expected_status_code: int) -> bool:
        return response.status_code == expected_status_code

    @staticmethod
    def verify_response_key_exists(response: requests.models.Response, __key: str) -> bool:
        json_dict = json.loads(response.content)
        return __key in json_dict

    @staticmethod
    def verify_response_key_value(response: requests.models.Response, __key: str, __value) -> bool:
        json_dict = json.loads(response.content)
        if __key in json_dict:
            return json_dict[__key] == __value
        else:
            raise AssertionError(f"{__key} in not in the response content!")

    @staticmethod
    def verify_response_key_value_class(response: requests.models.Response, __key: str, __class) -> bool:
        json_dict = json.loads(response.content)
        if __key in json_dict:
            try:
                __class(json_dict[__key])
                return True
            except ValueError:
                return False
        else:
            raise AssertionError(f"{__key} in not in the response content!")

    @staticmethod
    def verify_response_content(response, expected_content) -> bool:
        response_dict = json.loads(response.content)
        return response_dict == expected_content

    @staticmethod
    def get_value_from_response(response, __key):
        json_dict = json.loads(response.content)
        if __key in json_dict:
            return json_dict[__key]
        else:
            return None

    @staticmethod
    def verify_response_data_length(response: requests.models.Response, expected_length) -> bool:
        json_dict = json.loads(response.content)
        return len(json_dict.keys()) == expected_length
