from .attributes import AttributesResource
from .contacts import ContactsResource
from .exports import ExportsResource
from .imports import ImportsResource
from .segments import SegmentsResource

__all__ = ["AttributesResource",
           "ContactsResource",
           "ExportsResource",
           "ImportsResource",
           "SegmentsResource"]

RESOURCE_CLASSES = {
    "attributes": AttributesResource,
    "contacts": ContactsResource,
    "exports": ExportsResource,
    "imports": ImportsResource,
    "segments": SegmentsResource
}