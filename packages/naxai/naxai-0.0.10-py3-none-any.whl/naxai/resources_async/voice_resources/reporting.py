from naxai.resources_async.voice_resources.reporting_resources.outbound import OutboundResource
from naxai.resources_async.voice_resources.reporting_resources.inbound import InboundResource
from naxai.resources_async.voice_resources.reporting_resources.transfer import TransferResource

class ReportingResource:
    """ reporting resource for voice resource """
    
    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/reporting/metrics"
        self.outbound: OutboundResource = OutboundResource(self._client, self.root_path)
        self.inbound: InboundResource = InboundResource(self._client, self.root_path)
        self.transfer: TransferResource = TransferResource(self._client, self.root_path)
