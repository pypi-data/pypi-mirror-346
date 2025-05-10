import logging
import time
import os
from naxai.config import AUTH_URL, NAXAI_API_VERSION
from naxai.base.exceptions import NaxaiValueError

class BaseClient:
    """
    Base logic shared between sync and async clients.
    """

    def __init__(self,
                 api_client_id: str = None,
                 api_client_secret: str = None,
                 api_version: str = None,
                 auth_url: str = None,
                 logger = None):
        
        self.logger = logger or self._setup_default_logger()

        if not api_client_id:
            self.logger.info("api_client_id not provided, attempting to read from environment variable NAXAI_CLIENT_ID")
            self.api_client_id = os.getenv("NAXAI_CLIENT_ID", None)
            if not self.api_client_id:
                self.logger.warning("api_client_id not provided and could not be read from environment variable NAXAI_CLIENT_ID")
                raise NaxaiValueError("api_client_id is required")
        else:
            self.api_client_id = api_client_id

        if not api_client_secret:
            self.logger.info("api_client_secret not provided, attempting to read from environment variable NAXAI_SECRET")
            self.api_client_secret = os.getenv("NAXAI_SECRET", None)
            if not self.api_client_secret:
                self.logger.warning("api_client_secret not provided and could not be read from environment variable NAXAI_SECRET")
                raise NaxaiValueError("api_client_secret is required")
        else:
            self.api_client_secret = api_client_secret

        if not api_version:
            self.logger.info("api_version not provided, attempting to read from environment variable NAXAI_API_VERSION")
            self.api_version = os.getenv("NAXAI_API_VERSION", NAXAI_API_VERSION)
            if not self.api_version:
                self.logger.warning("api_version not provided and could not be read from environment variable NAXAI_API_VERSION")
                raise NaxaiValueError("api_version is required")
        else:
            self.api_version = api_version
            
        self.logger.debug("auth_url: %s", auth_url)

        if not auth_url:
            self.auth_url = os.getenv("NAXAI_AUTH_URL", AUTH_URL)
            if not self.auth_url:
                raise NaxaiValueError("auth_url is required")
        else:
            self.auth_url = auth_url
            
        self.logger.debug("self.auth_url: %s", self.auth_url)

        self.token: str = None
        self.token_expiry: int = 0

    def _setup_default_logger(self):
        logger = logging.getLogger("naxai")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)
        logger.propagate = False
        return logger
    
    def _is_token_valid(self) -> bool:
        return self.token and (self.token_expiry - time.time()) > 60  # 1 min buffer