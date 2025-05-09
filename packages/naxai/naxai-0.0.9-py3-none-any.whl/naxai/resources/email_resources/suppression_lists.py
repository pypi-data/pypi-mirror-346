from .suppression_lists_resources.unsubscribes import UnsubscribesResource
from .suppression_lists_resources.bounces import BouncesResource

class SuppressionListsResource:
    """ suppressionlists resource for email resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/suppression-lists"
        self.unsubscribes = UnsubscribesResource(client, self.root_path)
        self.bounces = BouncesResource(client, self.root_path)
        