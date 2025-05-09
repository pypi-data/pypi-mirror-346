from .reporting_resources.metrics import MetricsResource
from .reporting_resources.clicked_urls import ClickedUrlsResource

class ReportingResource:

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/reporting"
        self.metrics = MetricsResource(client, self.root_path)
        self.cliqued_urls = ClickedUrlsResource(client, self.root_path)