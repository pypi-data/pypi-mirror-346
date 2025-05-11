import requests
from typing import Optional, Dict, TypedDict
import threading
from bruce_models.api.api import Api
from bruce_models.api.guardian_api import GuardianApi

class BruceApiParams(TypedDict):
    """
    Represents the parameters for the Bruce API.
    """
    base_url: Optional[str]
    session_id: Optional[str]
    account_id: Optional[str]
    env: Optional[str]
    guardian: Optional[GuardianApi]

class BruceApi:
    """
    A basic API wrapper for making HTTP requests.
    """
    def __init__(self, params: BruceApiParams):
        self._loading = True
        self._lock = threading.Lock()
        self._init(params)

    @property
    def loading(self) -> bool:
        return self._loading

    def _init(self, params):
        try:
            # If no env was supplied, set to PROD.
            self.env = params.get("env", "PROD")
            self.base_url = params.get("base_url")
            self.session_id = params.get("session_id")
            self.account_id = params.get("account_id")

            # If no base_url was supplied, but an account_id was, we can request for it.
            if not self.base_url and self.account_id:
                # Use Guardian instance if was supplied, if not, create one.
                guardian = params.get("guardian", GuardianApi({ "env": self.env, "session_id": self.session_id }))
                account = guardian.GET(f"account/{self.account_id}")
                self.base_url = account.get("URL").get("Base")
            elif not self.base_url:
                raise ValueError("A valid base URL or account ID is required.")
            
            self._loading = False
        except Exception as e:
            self._loading = False
            raise e

    def set_session_id(self, session_id: str):
        """
        Sets the x-sessionid header for all future requests.
        """
        self.session_id = session_id

    def get_env(self):
        """
        Returns the current environment.
        """
        return self.env

    def _build_headers(self) -> Dict[str, str]:
        """
        Builds the headers for all requests that are sent.
        """
        headers = {
            "Content-Type": "application/json"
        }
        if self.session_id:
            headers["x-sessionid"] = self.session_id
        return headers

    def get(self, url: str, params: dict = {}) -> Dict:
        """
        Sends a GET request to the API.
        The URL should be absolute.
        """
        self._wait_for_loading()
        response = requests.get(url, headers=self._build_headers(), params=params)
        return Api.parse_result(response)

    def GET(self, url: str, params: dict = {}) -> Dict:
        """
        Sends a GET request to the API.
        The URL should be relative to the base URL.
        """
        self._wait_for_loading()
        return self.get(Api.join_url(self.base_url, url), params)
    
    def post(self, url: str, data: dict = {}, params: dict = {}) -> Dict:
        """
        Sends a POST request to the API.
        The URL should be absolute.
        """
        self._wait_for_loading()
        response = requests.post(url, headers=self._build_headers(), json=data, params=params)
        return Api.parse_result(response)
    
    def POST(self, url: str, data: dict = {}, params: dict = {}) -> Dict:
        """
        Sends a POST request to the API.
        The URL should be relative to the base URL.
        """
        self._wait_for_loading()
        return self.post(Api.join_url(self.base_url, url), data, params)

    def put(self, url: str, data: dict = {}, params: dict = {}) -> Dict:
        """
        Sends a PUT request to the API.
        The URL should be absolute.
        """
        self._wait_for_loading()
        response = requests.put(url, headers=self._build_headers(), json=data, params=params)
        return Api.parse_result(response)
    
    def PUT(self, url: str, data: dict = {}, params: dict = {}) -> Dict:
        """
        Sends a PUT request to the API.
        The URL should be relative to the base URL.
        """
        self._wait_for_loading()
        return self.put(Api.join_url(self.base_url, url), data, params)
    
    def delete(self, url: str, params: dict = {}) -> Dict:
        """
        Sends a DELETE request to the API.
        The URL should be absolute.
        """
        self._wait_for_loading()
        response = requests.delete(url, headers=self._build_headers(), params=params)
        return Api.parse_result(response)
    
    def DELETE(self, url: str, params: dict = {}) -> Dict:
        """
        Sends a DELETE request to the API.
        The URL should be relative to the base URL.
        """
        self._wait_for_loading()
        return self.delete(Api.join_url(self.base_url, url), params)

    def _wait_for_loading(self):
        """
        Blocks further requests until the loading state is set to False.
        This method will prevent further requests until initialization is complete.
        """
        with self._lock:
            while self._loading:
                pass