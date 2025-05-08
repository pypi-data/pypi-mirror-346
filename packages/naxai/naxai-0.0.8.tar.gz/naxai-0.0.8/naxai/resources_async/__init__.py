from .voice import VoiceResource
from .calendars import CalendarsResource
from .email import EmailResource
from .people import PeopleResource
from .sms import SMSResource

RESOURCE_CLASSES = {
    "voice": VoiceResource,
    "calendars": CalendarsResource,
    "email": EmailResource,
    "people": PeopleResource,
    "sms": SMSResource
}