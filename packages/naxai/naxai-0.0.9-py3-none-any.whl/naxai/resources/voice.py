from .voice_resources.call import CallResource
from .voice_resources.broadcast import BroadcastsResource
from .voice_resources.reporting import ReportingResource
from .voice_resources.activity_logs import ActivityLogsResource

class VoiceResource:
    """
    Provides access to voice related API actions.
    """

    def __init__(self, client):
        self._client = client
        self.root_path = "/voice"
        self.call: CallResource = CallResource(client, self.root_path)
        self.broadcasts: BroadcastsResource = BroadcastsResource(client, self.root_path)
        self.reporting: ReportingResource = ReportingResource(client, self.root_path)
        self.activity_logs: ActivityLogsResource = ActivityLogsResource(client, self.root_path)
