from config import *
import logging
import requests
import time


class GetHue:

    def __init__(self):
        self.config = Config()
        self.token = None
        self.refreshToken = None

    def __auth(self):
        response = requests.post(
            url=self.__get_url("/api/token/auth"),
            data={
                "username": self.config.username,
                "password": self.config.password,
            }
        )
        if response.status_code == 200:
            data = response.json()
            self.token = data["access"]
            self.refreshToken = data["refresh"]
        else:
            raise ApiException("Error authenticating into Hue", response)

    def __bearer(self):
        if self.token is None:
            self.__auth()
        return self.token

    def __get_url(self, endpoint):
        return self.config.api_url + endpoint

    def __headers(self):
        return {"Authorization": "Bearer " + self.__bearer()}

    def __get(self, endpoint, data):
        response = requests.get(
            url=self.__get_url(endpoint),
            headers=self.__headers(),
            data=data
        )
        logging.debug("GET %s (%d)", endpoint, response.status_code)
        return response

    def __post(self, endpoint, data):
        response = requests.post(
            url=self.__get_url(endpoint),
            headers=self.__headers(),
            data=data
        )
        logging.debug("POST %s (%d)", endpoint, response.status_code)
        return response

    def check_status(self, operation):
        response = self.__post(
            endpoint="/api/editor/check_status",
            data={
                "operationId": operation
            }
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise ApiException("Error while calling: check_status", response)

    def execute_hive(self, statement):
        response = self.__post(
            endpoint="/api/editor/execute/hive",
            data={
                "statement": statement
            }
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise ApiException("Error while calling: execute_hive", response)

    def execute_hive_sync(self, statement, retries=30, interval=1):
        query = self.execute_hive(statement)
        operation_id = query["history_uuid"]
        while --retries > 0:
            time.sleep(interval)
            check = self.check_status(operation_id)
            if check["status"] == 0:
                return self.fetch_result_data(operation_id)
        raise ApiException("Timeout while waiting for result")

    def fetch_result_data(self, operation):
        response = self.__post(
            endpoint="/api/editor/fetch_result_data",
            data={
                "operationId": operation
            }
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise ApiException("Error while calling: fetch_result_data", response)


class ApiException(Exception):

    def __init__(self, message, response):
        self.message = message
        self.response = response
