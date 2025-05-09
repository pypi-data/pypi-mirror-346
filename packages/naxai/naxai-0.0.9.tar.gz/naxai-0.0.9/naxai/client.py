import time
import os
from typing import Any
import httpx
from naxai.base.base_client import BaseClient
from naxai.base.exceptions import (NaxaiAuthenticationError,
                                   NaxaiAuthorizationError,
                                   NaxaiResourceNotFound,
                                   NaxaiRateLimitExceeded,
                                   NaxaiAPIRequestError,
                                   NaxaiValueError,
                                   NaxaiInvalidRequestError)
from naxai.models.token_response import TokenResponse
from naxai.resources.voice import VoiceResource
from naxai.resources.calendars import CalendarsResource
from naxai.resources.email import EmailResource
from naxai.resources.sms import SMSResource
from .config import API_BASE_URL


class NaxaiClient(BaseClient):
    """
    Naxai Client for interacting with Voice, SMS, Email, Calendars and People API.
    """

    def __init__(self,
                 api_client_id: str = None,
                 api_client_secret: str = None,
                 api_version: str = None,
                 auth_url: str = None,
                 api_base_url: str = None,
                 logger=None):
        super().__init__(api_client_id, api_client_secret, api_version, auth_url, logger)

        if not api_base_url:
            self.api_base_url = os.getenv("NAXAI_API_URL", API_BASE_URL)
            if not self.api_base_url:
                raise NaxaiValueError("api_base_url is required")
        else:
            self.api_base_url = api_base_url
            
        self._http = httpx.Client()
        self.voice = VoiceResource(self)
        self.calendars = CalendarsResource(self)
        self.email = EmailResource(self)
        self.sms = SMSResource(self)

    def _authenticate(self):
        self.logger.debug(f"Authenticating using auth_url: {getattr(self, 'auth_url', 'MISSING')}")
        if self._is_token_valid():
            return

        payload = {
            "client_id": self.api_client_id,
            "client_secret": self.api_client_secret,
            "grant_type": "client_credentials",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = self._http.post(self.auth_url, data=payload, headers=headers)
        
        if response.is_error:
            raise NaxaiAuthenticationError(f"Authentication failed: {response.text}", status_code=response.status_code)
        
        data = TokenResponse.model_validate(response.json())
        self.token = data.access_token
        self.token_expiry = time.time() + data.expires_in
        self.logger.info("Authenticated successfully, token valid for 24h.")

    def _request(self, method: str, path: str, **kwargs) -> Any:
        self._authenticate()

        headers = kwargs.pop("headers", {})
        headers.update({"Authorization": f"Bearer {self.token}",
                        "X-version": self.api_version})

        url = f"{self.api_base_url.rstrip('/')}/{path.lstrip('/')}"
        response = self._http.request(method, url, headers=headers, **kwargs)

        if response.is_error:
            self._handle_error(response)  # Handle errors as usual

        if response.status_code == 204:
            return None

        return response.json()

    def _handle_error(self, response: httpx.Response):
        try:
            error_data = response.json().get("error", {})
        except Exception:
            error_data = {}

        code = error_data.get("code")
        message = error_data.get("message", response.text)
        details = error_data.get("details")

        exc_args = {"message": message, "status_code": response.status_code, "error_code": code, "details": details}

        if response.status_code == 401:
            raise NaxaiAuthenticationError(**exc_args)
        elif response.status_code == 403:
            raise NaxaiAuthorizationError(**exc_args)
        elif response.status_code == 404:
            raise NaxaiResourceNotFound(**exc_args)
        elif response.status_code == 422:
            raise NaxaiInvalidRequestError(**exc_args)
        elif response.status_code == 429:
            raise NaxaiRateLimitExceeded(**exc_args)
        else:
            raise NaxaiAPIRequestError(**exc_args)

    def close(self):
        self._http.close()  # Close the sync client
