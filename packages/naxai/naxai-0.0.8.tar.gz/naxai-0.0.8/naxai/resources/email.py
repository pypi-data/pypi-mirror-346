from .email_resources.transactional import TransactionalResource
from .email_resources.activity_logs import ActivityLogsResource
from .email_resources.domains import DomainsResource
from .email_resources.newsletters import NewslettersResource
from .email_resources.reporting import ReportingResource
from .email_resources.sender_identities import SenderIdentitiesResource
from .email_resources.suppression_lists import SuppressionListsResource
from .email_resources.templates import TemplatesResource
from .email_resources import RESOURCE_CLASSES


class EmailResource:
    """
    Provides access to email related API actions.
    """

    def __init__(self, client):
        self._client = client
        self.root_path = "/email"
        self.transactional: TransactionalResource = TransactionalResource(self._client, self.root_path)
        self.activity_logs: ActivityLogsResource = ActivityLogsResource(self._client, self.root_path)
        self.domains: DomainsResource = DomainsResource(self._client, self.root_path)
        self.newsletters: NewslettersResource = NewslettersResource(self._client, self.root_path)
        self.reporting: ReportingResource = ReportingResource(self._client, self.root_path)
        self.sender_identities: SenderIdentitiesResource = SenderIdentitiesResource(self._client, self.root_path)
        self.suppression_lists: SuppressionListsResource = SuppressionListsResource(self._client, self.root_path)
        self.templates: TemplatesResource = TemplatesResource(self._client, self.root_path)
