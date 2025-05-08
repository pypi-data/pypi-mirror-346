from .people_resources import RESOURCE_CLASSES
from .people_resources.attributes import AttributesResource
from .people_resources.contacts import ContactsResource
from .people_resources.exports import ExportsResource
from .people_resources.imports import ImportsResource
from .people_resources.segments import SegmentsResource

class PeopleResource:
    """
    Provides access to people related API actions.
    """

    def __init__(self, client):
        self._client = client
        self.root_path = "/people"
        self.attributes: AttributesResource = AttributesResource(self._client, self.root_path)
        self.contacts: ContactsResource = ContactsResource(self._client, self.root_path)
        self.exports: ExportsResource = ExportsResource(self._client, self.root_path)
        self.imports: ImportsResource = ImportsResource(self._client, self.root_path)
        self.segments: SegmentsResource = SegmentsResource(self._client, self.root_path)
