from .activity_logs import ActivityLogsResource
from .domains import DomainsResource
from .newsletters import NewslettersResource
from .reporting import ReportingResource
from .sender_identities import SenderIdentitiesResource
from .suppression_lists import SuppressionListsResource
from .templates import TemplatesResource
from .transactional import TransactionalResource

__all__ = [
    "ActivityLogsResource",
    "DomainsResource",
    "NewslettersResource",
    "ReportingResource",
    "SenderIdentitiesResource",
    "SuppressionListsResource",
    "TemplatesResource",
    "TransactionalResource",
]

RESOURCE_CLASSES = {
    "activity_logs": ActivityLogsResource,
    "domains": DomainsResource,
    "newsletters": NewslettersResource,
    "reporting": ReportingResource,
    "sender_identities": SenderIdentitiesResource,
    "suppression_lists": SuppressionListsResource,
    "templates": TemplatesResource,
    "transactional": TransactionalResource,
}