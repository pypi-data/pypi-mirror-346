#-------------------------------------------------------------------------------#
#
#                         --- p y C o l d S t r e a m ---
#
#-------------------------------------------------------------------------------#

import logging
import secrets
import requests
import json
import time
import os

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

# Local storage for the hosting location
_HOST = None

                 #-----------------------------------------------#
                 #                    Set the hosting location
                 #-----------------------------------------------#

## Set the hosting location
#
# @param host (str): the hosting location
def set_hosting(host):
    global _HOST

    if host in ["ap1", "eu1", "us1"]:
        _HOST = f"{host}.coldstream" 
    else:
        log.error("Unknown hosting location! Valid options are ['ap1', 'eu1', 'us1'].")
        _HOST = host

                 #-----------------------------------------------#
                 #                    ColdstreamRestClient
                 #-----------------------------------------------#

## Main case data class
class ColdStreamRestClient:

                 #------------------- Attributes ----------------#

    ## @start_attributes

    ## Return the api token
    @property
    def token(self):
        return self.__token

    ## Return the base URL
    @property
    def URL(self):
        return {"identity"     : f"https://identity.{_HOST}.diabatix.com",
                "projects"     : f"https://project.{_HOST}.diabatix.com",
                "cases"        : f"https://case.{_HOST}.diabatix.com",
                "targets"      : f"https://case.{_HOST}.diabatix.com",
                "organizations": f"https://case.{_HOST}.diabatix.com",
                "regions"      : f"https://case.{_HOST}.diabatix.com",
                "subregions"   : f"https://case.{_HOST}.diabatix.com",
                "boundaries"   : f"https://case.{_HOST}.diabatix.com",
                "interfaces": f"https://case.{_HOST}.diabatix.com",
                "fileserver"   : f"https://fileserver.{_HOST}.diabatix.com"}

    ## @end_attributes

                 #------------------- Constructor ---------------#

    ## Constructor
    #
    # @param user (str, optional): username, defaults to None
    # @param password (str, optional): password, defaults to None
    # @param token (str, optionla): API key, defaults to None
    def __init__(self, user=None, password=None, token=token):
        
        self.__token = token

        if user is not None and password is not None:
            self._create_basic_session(user, password)

        if self.__token is None:
            raise ApiError(f"Failed to initialize {self.__class__.__name__}")

                 #--------------------- Methods -----------------#

    ## Initiate the client based on username password combination
    def _create_basic_session(self, user, password):
        log.info("Connecting to ColdStream...")

        url_login = self.URL["identity"] + "/account/login"
        payload = json.dumps({"email": user, "password": password})

        id_token = secrets.token_hex(15)
        headers = {
            "accept": "application/json",
            "content-type": "application/*+json",
            "Authorization": id_token
        }
        response = self._response_handler(requests.post(
            url_login,
            headers=headers,
            data=payload
        ))

        if response is None:
            raise ApiError("Failed to login to ColdStream!")
        else:
            if "mfaToken" in response:
                mfa_token = response["mfaToken"]
                url_req = url_login + "/otp"

                while(True):
                    mfa_code = input("Enter MFA Code:")
                    payload = json.dumps({"otp" : mfa_code,
                                          "mfaToken" : mfa_token})

                    response = self._response_handler(requests.post(
                        url_req,
                        headers=headers,
                        data=payload
                    ))
                    if response and "accessToken" in response:
                        break

            self.__token = response["accessToken"]

        log.info("Connected!")

    ## Handle the response
    #
    # @return (dict)
    @staticmethod
    def _response_handler(response):
        if response.ok:
            if response.text:
                return response.json()
            else:
                return None

        raise ApiError(f"API Error {response.status_code}: {response.text}")

    ## Get request
    #
    # @param url (str): the request url
    def request_del(self, url):
        return self._response_handler(requests.get(
            url,
            headers={"Authorization": f"Bearer {self.token}"}
        ))

    ## Patch request
    #
    # @param url (str): the request url
    def request_patch(self, url):
        return self._response_handler(requests.patch(
            url,
            headers={"Authorization": f"Bearer {self.token}"}
        ))

    ## Get request
    #
    # @param url (str): the request url
    def request_get(self, url):
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        return self._response_handler(requests.get(
            url,
            headers=headers
        ))

    ## Put request, typically for updating an existing entry
    #
    # @param url (str): the request url
    # @param payload (dict): the payload
    def request_put(self, url, payload):
        headers = {
            "accept": "application/json",
            "content-type": "application/*+json",
            "Authorization": f"Bearer {self.token}"
        }

        raw_payload = json.dumps(payload)
        return self._response_handler(requests.put(
            url,
            data=raw_payload,
            headers=headers
        ))

    ## Post request, for creating a new entry
    #
    # @param url (str): the request url
    # @param payload (dict): the payload
    def request_post(self, url, payload):
        headers = {
            "accept": "application/json",
            "content-type": "application/*+json",
            "Authorization": f"Bearer {self.token}"
        }
        raw_payload = json.dumps(payload)
        return self._response_handler(requests.post(
            url,
            data=raw_payload,
            headers=headers
        ))

    ## Downloads a file from a given presigned url
    #
    # @param presigned_url (str): a presigned file url to the file you want to download
    # @param filename (str): local target filename
    def download_file(self, presigned_url, filename):
        response = requests.get(presigned_url, stream=True)

        if response.status_code == 200:
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        else:
            raise ApiError(f"Failed to download file {presigned_url}")

    ## Upload a file to the given url. The url must be a presigned url.
    #
    # @param filepath (str): path to the file
    # @param presigned_url (str): a presigned file url to the target path
    def upload_file(self, filepath, presigned_url):
        # Read the file
        with open(filepath, 'rb') as file:
            file_data = file.read()

        headers = {
            "content-type": "application/octet-stream",
        }
        return self._response_handler(requests.put(
            presigned_url,
            data=file_data,
            headers=headers
        ))

#-------------------------------------------------------------------------------#

                 #-----------------------------------------------#
                 #                    ColdStreamDataObject
                 #-----------------------------------------------#

## Manage a ColdStream data object
class ColdStreamDataObject(ColdStreamRestClient):


                 #------------------- Attributes ----------------#

    ## @start_attributes

    ## Return the region ID
    @property
    def ID(self):
        return self.data["id"]

    ## Return the raw data
    #
    # @return (dict)
    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

	## Return the instance url
    @property
    def instance_url(self):
        return self.URL[self.__resource] + f"/{self.__resource}/{self.ID}"

    ## @end_attributes

                 #------------------- Constructor ---------------#

    ## Constructor
    #
    # @param token (str): the api token
    # @param data (dict): case data
    # @param resource (str): resource key
    def __init__(self, token, data, resource):
        super().__init__(token=token)
        self.__data = data
        self.__resource = resource

                 #--------------------- Methods -----------------#

    ## Define string representation
    def __str__(self):
        return f"ID {self.ID}\n{self.data}"

    ## Delete the instance
    def delete(self):
        self.request_del(self.instance_url)

    ## Update the instance with the given payload
    #
    # @param payload (dict): the request payload
    def update(self, payload):
        self.__data = self.request_put(self.instance_url, payload)

    ## Create a signed url
    #
    # @param filepath (str): path to the file
    # @param case_ID (int): id of the case you want to upload a file to
    # @param compoent_ID (int): id of the component that you want to upload a file for, defaults to None
    #
    # @return (dict)
    def get_signed_url(self, filepath, case_ID, component_ID=None):
        size = os.path.getsize(filepath)
        filename = os.path.basename(filepath)

        url = self.URL["fileserver"] + "/cases/" + str(case_ID) + "/files"
        payload = {"fileName" : filename,
                   "fileSize" : size,
                   "caseComponentId" : component_ID}

        return self.request_post(url, payload)

    ## Create the visualization file from a previously uploaded file.
    #
    # @param case_ID (int): id of the case
    # @param file_ID (int): id of the file you want to visualize
    # @param file_url (str): url to the file you want to convert
    #
    # @returns (dict): a json object with meta data for the job
    def create_visualization(self, case_ID, file_ID, file_url):
        url = self.URL["cases"] + "/jobs/convert"
        payload = json.dumps({"caseId" : case_ID,
                              "fileId" : file_ID,
                              "fileURL" : file_url})
        headers = {
            "accept": "application/json",
            "content-type": "application/*+json",
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.post(url, data=payload, headers=headers)

        if response.ok:
            return response.json()
        else:
            if b"Job already runs for case" in response.content:
                log.info("A job is already running, retrying in 2s")
                time.sleep(2)
                return self.create_visualization(case_ID, file_ID, file_url)
            else:
                raise ApiError(reason="File upload failed")

        return None

#-------------------------------------------------------------------------------#

                 #-----------------------------------------------#
                 #                    ApiError
                 #-----------------------------------------------#

## Manage a ColdStream data object
class ApiError(Exception):


                 #------------------- Attributes ----------------#

    ## @start_attributes

    ## @end_attributes

                 #------------------- Constructor ---------------#

    ## Constructor
    #
    # @param msg (str): the error message
    def __init__(self, msg):
        super().__init__(msg)
        log.error(f"{msg}")

#-------------------------------------------------------------------------------#
