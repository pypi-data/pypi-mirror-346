from .call import CallResource
from .broadcast import BroadcastsResource
from .reporting import ReportingResource
from .activity_logs import ActivityLogsResource

RESOURCE_CLASSES = {
    "call": CallResource,
    "broadcasts": BroadcastsResource,
    "reporting": ReportingResource,
    "activity_logs": ActivityLogsResource
}