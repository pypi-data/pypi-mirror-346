from typing import Optional, Literal, Union, List
from pydantic import BaseModel, Field
from naxai.models.base.pagination import Pagination

CONDITIONS = Literal["eq",
                     "not-eq",
                     "gt",
                     "lt",
                     "exists",
                     "not-exists",
                     "contains",
                     "not-contains",
                     "is-true",
                     "is-false",
                     "is-timestamp",
                     "is-timestamp-before",
                     "is-timestamp-after",
                     "is-mobile",
                     "is-not-mobile"]


class EventPropertiesCondObject(BaseModel):
    """
    Model representing a condition for event properties in segment definitions.
    
    This class defines a single condition that can be applied to event properties
    when creating or updating segments in the Naxai People API.
    
    Attributes:
        name (str): The name of the event property to evaluate.
        operator (Literal): The comparison operator to use. Must be one of:
            "eq", "not-eq", "gt", "lt", "is-true", "is-false".
        value (Optional[Union[str, int, bool]]): The value to compare against.
            Required for all operators except "is-true" and "is-false".
    
    Example:
        >>> # Create a condition for event property "purchase_amount" greater than 100
        >>> condition = EventPropertiesCondObject(
        ...     name="purchase_amount",
        ...     operator="gt",
        ...     value=100
        ... )
    """
    name: str
    operator: Literal["eq", "not-eq", "gt", "lt", "is-true", "is-false"]
    value: Optional[Union[str, int, bool]] = None

class EventProperties(BaseModel):
    """
    Model representing property conditions for events in segment definitions.
    
    This class defines a set of conditions that can be applied to event properties
    when creating or updating segments in the Naxai People API. It supports both
    "all" (AND) and "any" (OR) logical combinations of conditions.
    
    Attributes:
        all (Optional[list[EventPropertiesCondObject]]): List of conditions that must
            all be satisfied (AND logic).
        any (Optional[list[EventPropertiesCondObject]]): List of conditions where at
            least one must be satisfied (OR logic).
    
    Example:
        >>> # Create event properties where purchase_amount > 100 AND currency = "USD"
        >>> properties = EventProperties(
        ...     all=[
        ...         EventPropertiesCondObject(name="purchase_amount", operator="gt", value=100),
        ...         EventPropertiesCondObject(name="currency", operator="eq", value="USD")
        ...     ]
        ... )
    """
    all: Optional[list[EventPropertiesCondObject]]
    any: Optional[list[EventPropertiesCondObject]]

class EventObject(BaseModel):
    """
    Model representing an event condition in segment definitions.
    
    This class defines conditions related to events that contacts have triggered,
    used when creating or updating segments in the Naxai People API.
    
    Attributes:
        name (str): The name of the event to evaluate.
        count (int): The number of times the event should have occurred. Defaults to 1.
        count_boundary (Literal): Whether the count should be at least or at most the specified value.
            Must be either "at-least" or "at-most". Defaults to "at-least".
        time_boundary (Literal): The time frame to consider for the events.
            Must be one of "all-time", "within-last", "before", "after". Defaults to "all-time".
        period_boundary (Literal): The unit of time for time_boundary.
            Must be either "day" or "month". Defaults to "day".
        interval_boundary (int): The number of time units for time_boundary.
            Must be between 1 and 366. Defaults to 1.
        date (Optional[int]): A timestamp to use with "before" or "after" time boundaries.
        properties (EventProperties): Additional conditions on the event properties.
    
    Example:
        >>> # Create a condition for users who made at least 2 purchases in the last 30 days
        >>> event = EventObject(
        ...     name="purchase",
        ...     count=2,
        ...     count_boundary="at-least",
        ...     time_boundary="within-last",
        ...     period_boundary="day",
        ...     interval_boundary=30,
        ...     properties=EventProperties(
        ...         all=[EventPropertiesCondObject(name="status", operator="eq", value="completed")]
        ...     )
        ... )
    """
    name: str
    count: int = Field(default=1)
    count_boundary: Literal["at-least", "at-most"] = Field(default="at-least", alias="countBoundary")
    time_boundary: Literal["all-time", "within-last", "before", "after"] = Field(default="all-time", alias="timeBoundary")
    period_boundary: Literal["day", "month"] = Field(default="day", alias="periodBoundary")
    interval_boundary: int = Field(default=1, alias="intervalBoundary", ge=1, le=366)
    date: Optional[int] = None
    properties: EventProperties

class AttributeArrayObject(BaseModel):
    """
    Model representing an attribute condition with an array of values.
    
    This class defines conditions for attributes that require multiple values,
    such as range comparisons, used in segment definitions.
    
    Attributes:
        operator (Literal): The comparison operator to use. Must be either
            "between" or "is-timestamp-between".
        field (str): The name of the attribute field to evaluate.
        values (list): A list of exactly two values defining the range.
            For "between", these are the min and max values.
            For "is-timestamp-between", these are the start and end timestamps.
    
    Example:
        >>> # Create a condition for age between 25 and 35
        >>> condition = AttributeArrayObject(
        ...     operator="between",
        ...     field="age",
        ...     values=[25, 35]
        ... )
    """
    operator: Literal["between", "is-timestamp-between"]
    field: str
    values: list = Field(min_length=2, max_length=2)

class AttributeObject(BaseModel):
    """
    Model representing a simple attribute condition in segment definitions.
    
    This class defines conditions for attributes that require a single value comparison,
    used when creating or updating segments in the Naxai People API.
    
    Attributes:
        operator (CONDITIONS): The comparison operator to use. Must be one of the
            operators defined in the CONDITIONS Literal.
        field (str): The name of the attribute field to evaluate.
        value (Optional[Union[str, int, bool]]): The value to compare against.
            Required for most operators except existence checks like "exists".
    
    Example:
        >>> # Create a condition for country equals "US"
        >>> condition = AttributeObject(
        ...     operator="eq",
        ...     field="country",
        ...     value="US"
        ... )
    """
    operator: CONDITIONS
    field: str
    value: Optional[Union[str, int, bool]]

class EventCond(BaseModel):
    """
    Model representing an event condition wrapper in segment definitions.
    
    This class serves as a wrapper for EventObject instances to be used in
    condition groups within segment definitions.
    
    Attributes:
        event (EventObject): The event condition to apply.
    
    Example:
        >>> # Create an event condition for a purchase event
        >>> event_obj = EventObject(
        ...     name="purchase",
        ...     properties=EventProperties(
        ...         all=[EventPropertiesCondObject(name="amount", operator="gt", value=50)]
        ...     )
        ... )
        >>> condition = EventCond(event=event_obj)
    """
    event: EventObject = Field(default=None)

class AttributeCondArray(BaseModel):
    """
    Model representing an attribute array condition wrapper in segment definitions.
    
    This class serves as a wrapper for AttributeArrayObject instances to be used in
    condition groups within segment definitions.
    
    Attributes:
        attribute (AttributeArrayObject): The attribute array condition to apply.
    
    Example:
        >>> # Create an attribute condition for age between 25 and 35
        >>> attr_obj = AttributeArrayObject(
        ...     operator="between",
        ...     field="age",
        ...     values=[25, 35]
        ... )
        >>> condition = AttributeCondArray(attribute=attr_obj)
    """
    attribute: AttributeArrayObject = Field(default=None)

class AttributeCondSimple(BaseModel):
    """
    Model representing a simple attribute condition wrapper in segment definitions.
    
    This class serves as a wrapper for AttributeObject instances to be used in
    condition groups within segment definitions.
    
    Attributes:
        attribute (AttributeObject): The simple attribute condition to apply.
    
    Example:
        >>> # Create an attribute condition for country equals "US"
        >>> attr_obj = AttributeObject(
        ...     operator="eq",
        ...     field="country",
        ...     value="US"
        ... )
        >>> condition = AttributeCondSimple(attribute=attr_obj)
    """
    attribute: AttributeObject = Field(default=None)

class AllCondGroup(BaseModel):
    """
    Model representing a group of conditions that must all be satisfied.
    
    This class defines a group of conditions that are combined with AND logic,
    meaning all conditions must be satisfied for the group to evaluate to true.
    
    Attributes:
        all (list[Union[AttributeCondSimple, AttributeCondArray, EventCond]]): List of
            conditions that must all be satisfied.
    
    Example:
        >>> # Create a condition group where country is "US" AND age is between 25 and 35
        >>> country_cond = AttributeCondSimple(
        ...     attribute=AttributeObject(operator="eq", field="country", value="US")
        ... )
        >>> age_cond = AttributeCondArray(
        ...     attribute=AttributeArrayObject(operator="between", field="age", values=[25, 35])
        ... )
        >>> condition_group = AllCondGroup(all=[country_cond, age_cond])
    """
    all: list[Union[AttributeCondSimple, AttributeCondArray, EventCond]]

class AnyCondGroup(BaseModel):
    """
    Model representing a group of conditions where any can be satisfied.
    
    This class defines a group of conditions that are combined with OR logic,
    meaning at least one condition must be satisfied for the group to evaluate to true.
    
    Attributes:
        any (list[Union[AttributeCondSimple, AttributeCondArray, EventCond]]): List of
            conditions where at least one must be satisfied.
    
    Example:
        >>> # Create a condition group where country is "US" OR country is "CA"
        >>> us_cond = AttributeCondSimple(
        ...     attribute=AttributeObject(operator="eq", field="country", value="US")
        ... )
        >>> ca_cond = AttributeCondSimple(
        ...     attribute=AttributeObject(operator="eq", field="country", value="CA")
        ... )
        >>> condition_group = AnyCondGroup(any=[us_cond, ca_cond])
    """
    any: list[Union[AttributeCondSimple, AttributeCondArray, EventCond]]

class Condition(BaseModel):
    """
    Model representing the complete condition structure for segment definitions.
    
    This class defines the top-level condition structure used in segment definitions,
    supporting both "all" (AND) and "any" (OR) logical combinations of conditions
    and condition groups.
    
    Attributes:
        all (Optional[list[Union[AttributeCondSimple, AttributeCondArray, EventCond, AllCondGroup, AnyCondGroup]]]): 
            List of conditions that must all be satisfied (AND logic).
        any (Optional[list[Union[AttributeCondSimple, AttributeCondArray, EventCond, AllCondGroup, AnyCondGroup]]]): 
            List of conditions where at least one must be satisfied (OR logic).
    
    Example:
        >>> # Create a condition where (country is "US" AND age > 21) OR has made a purchase
        >>> country_cond = AttributeCondSimple(
        ...     attribute=AttributeObject(operator="eq", field="country", value="US")
        ... )
        >>> age_cond = AttributeCondSimple(
        ...     attribute=AttributeObject(operator="gt", field="age", value=21)
        ... )
        >>> purchase_cond = EventCond(
        ...     event=EventObject(name="purchase", properties=EventProperties())
        ... )
        >>> 
        >>> # Group the country and age conditions with AND logic
        >>> country_age_group = AllCondGroup(all=[country_cond, age_cond])
        >>> 
        >>> # Combine with purchase condition using OR logic
        >>> condition = Condition(any=[country_age_group, purchase_cond])
    """
    all: Optional[list[Union[AttributeCondSimple, AttributeCondArray, EventCond, AllCondGroup, AnyCondGroup]]] = Field(default=None)
    any: Optional[list[Union[AttributeCondSimple, AttributeCondArray, EventCond, AllCondGroup, AnyCondGroup ]]] = Field(default=None)

class SegmentBaseModel(BaseModel):
    """
    Base model for segment objects in the Naxai People API.
    
    This class serves as the foundation for segment-related responses in the People API,
    providing the common fields that all segment objects share.
    
    Attributes:
        id (str): The unique identifier of the segment.
        name (str): The name of the segment.
        description (Optional[str]): A description of the segment's purpose or criteria.
            Maximum length is 300 characters.
        state (Optional[Literal["ready", "building"]]): The current state of the segment.
        predefined (Optional[bool]): Whether this is a predefined segment.
        condition (Optional[Condition]): The condition structure defining the segment's criteria.
        modified_by (Optional[str]): The ID of the user who last modified the segment.
            Mapped from the JSON key 'modifiedBy'.
        modified_at (Optional[int]): Timestamp when the segment was last modified.
            Mapped from the JSON key 'modifiedAt'.
        type_ (Optional[Literal["manual", "dynamic"]]): The type of segment.
            Mapped from the JSON key 'type'.
    
    Example:
        >>> # Create a basic segment
        >>> segment = SegmentBaseModel(
        ...     id="seg_123abc",
        ...     name="US Customers",
        ...     description="All customers from the United States",
        ...     state="ready",
        ...     type_="dynamic",
        ...     condition=Condition(
        ...         all=[
        ...             AttributeCondSimple(
        ...                 attribute=AttributeObject(operator="eq", field="country", value="US")
        ...             )
        ...         ]
        ...     )
        ... )
    
    Note:
        - This class is designed to be subclassed by specific segment response models
        - It uses populate_by_name=True to support both direct field names and aliases
        - The type field uses type_ to avoid conflict with Python's built-in type keyword
    """
    id: str
    name: str
    description: Optional[str] = Field(default=None, max_length=300)
    state: Optional[Literal["ready", "building"]] = Field(default=None)
    predefined: Optional[bool] = Field(default=None)
    condition: Optional[Condition] = Field(default=None)
    modified_by: Optional[str] = Field(default=None, alias="modifiedBy")
    modified_at: Optional[int] = Field(default=None, alias="modifiedAt")
    type_: Optional[Literal["manual", "dynamic"]] = Field(default=None, alias="type")

    model_config = {"populate_by_name": True}

class SegmentHistoryDay(BaseModel):
    """
    Model representing a single day's history for a segment.
    
    This class contains information about how a segment's membership changed on a specific day,
    including additions, removals, and the total count.
    
    Attributes:
        date (Optional[int]): The timestamp representing the day.
        added (Optional[int]): The number of contacts added to the segment on this day.
        removed (Optional[int]): The number of contacts removed from the segment on this day.
        change (Optional[int]): The net change in segment membership (added - removed).
        current (Optional[int]): The total number of contacts in the segment at the end of this day.
    
    Example:
        >>> # Create a history entry for a specific day
        >>> history_day = SegmentHistoryDay(
        ...     date=1703066400000,  # December 20, 2023
        ...     added=15,
        ...     removed=3,
        ...     change=12,
        ...     current=250
        ... )
    """
    date: Optional[int] = Field(default=None)
    added: Optional[int] = Field(default=None)
    removed: Optional[int] = Field(default=None)
    change: Optional[int] = Field(default=None)
    current: Optional[int] = Field(default=None)

class ContactBaseModel(BaseModel):
    """
    Base model for contact objects in the Naxai People API.
    
    This class represents a contact in the Naxai system, containing their basic
    identification and communication information.
    
    Attributes:
        nx_id (str): The unique Naxai identifier for the contact.
            Mapped from the JSON key 'nxId'.
        email (Optional[str]): The contact's email address.
        phone (Optional[str]): The contact's phone number.
        sms_capable (Optional[bool]): Whether the contact's phone number can receive SMS.
            Mapped from the JSON key 'smsCapable'.
        external_id (Optional[str]): An external identifier for the contact.
            Mapped from the JSON key 'externalId'.
        unsubscribed (Optional[bool]): Whether the contact has unsubscribed from communications.
        language (Optional[str]): The contact's preferred language.
        created_at (Optional[int]): Timestamp when the contact was created.
            Mapped from the JSON key 'createdAt'.
        created_at_naxai (Optional[int]): Timestamp when the contact was created in Naxai.
            Mapped from the JSON key 'createdAtNaxai'.
    
    Example:
        >>> # Create a basic contact
        >>> contact = ContactBaseModel(
        ...     nxId="cnt_123abc",
        ...     email="john.doe@example.com",
        ...     phone="+1234567890",
        ...     smsCapable=True,
        ...     externalId="cust_456",
        ...     language="en",
        ...     createdAt=1703066400000
        ... )
    
    Note:
        - This class uses populate_by_name=True to support both direct field names and aliases
        - The extra="allow" config allows additional fields to be included for custom attributes
    """
    nx_id: str = Field(alias="nxId")
    email: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    sms_capable: Optional[bool] = Field(alias="smsCapable", default=None)
    external_id: Optional[str] = Field(alias="externalId", default=None)
    unsubscribed: Optional[bool] = Field(default=None)
    language: Optional[str] = Field(default=None)
    created_at: Optional[int] = Field(alias="createdAt", default=None)
    created_at_naxai: Optional[int] = Field(alias="createdAtNaxai", default=None)

    model_config = {"populate_by_name": True,
                    "extra": "allow"}

class ListSegmentsResponse(BaseModel):
    """
    Response model for listing segments in the Naxai People API.
    
    This class represents the response returned by the API when retrieving a list of
    segments. It implements list-like behavior, allowing the response to be used
    as an iterable collection of segment objects.
    
    Attributes:
        root (List[SegmentBaseModel]): The list of segment objects returned by the API.
            Defaults to an empty list if no segments are found.
    
    Example:
        >>> # Creating a response with segment objects
        >>> segments = [
        ...     SegmentBaseModel(id="seg_123", name="US Customers"),
        ...     SegmentBaseModel(id="seg_456", name="High Value Customers")
        ... ]
        >>> response = ListSegmentsResponse(root=segments)
        >>> 
        >>> # Using list-like operations
        >>> len(response)  # Returns 2
        >>> response[0]    # Returns the first segment
        >>> for segment in response:  # Iterating through segments
        ...     print(segment.name)
        US Customers
        High Value Customers
        >>> 
        >>> # Parsing from JSON
        >>> json_data = '[{"id": "seg_123", "name": "US Customers"}, {"id": "seg_456", "name": "High Value Customers"}]'
        >>> response = ListSegmentsResponse.model_validate_json(json_data)
        >>> len(response)  # Returns 2
    
    Note:
        - This class implements __len__, __getitem__, and __iter__ methods to provide
          list-like behavior
        - The model_validate_json method handles both array-style JSON and object-style
          JSON with a root field
        - When a JSON array is provided, it's automatically wrapped in a 'root' field
        - The class uses Pydantic's default_factory to initialize the root as an empty
          list when no data is provided
    """
    root: List[SegmentBaseModel] = Field(default_factory=list)
    
    def __len__(self) -> int:
        """Return the number of segments in the list."""
        return len(self.root)
    
    def __getitem__(self, index):
        """Access segment by index."""
        return self.root[index]
    
    def __iter__(self):
        """Iterate through segments."""
        return iter(self.root)
    
    @classmethod
    def model_validate_json(cls, json_data: str, **kwargs):
        """Parse JSON data into the model.
        
        This method handles both array-style JSON and object-style JSON with a root field.
        
        Args:
            json_data (str): The JSON string to parse
            **kwargs: Additional arguments to pass to the standard model_validate_json method
            
        Returns:
            ListAttributesResponse: A validated instance of the class
        """
        import json
        data = json.loads(json_data)
        
        # If the data is a list, wrap it in a dict with the root field
        if isinstance(data, list):
            return cls(root=data)
        
        # Otherwise, use the standard Pydantic validation
        return super().model_validate_json(json_data, **kwargs)

class CreateSegmentResponse(SegmentBaseModel):
    """
    Response model for segment creation in the Naxai People API.
    
    This class represents the response returned by the API when a new segment is
    successfully created. It inherits all fields from SegmentBaseModel.
    
    Example:
        >>> response = CreateSegmentResponse(
        ...     id="seg_123abc",
        ...     name="New Customers",
        ...     description="Customers who joined in the last 30 days",
        ...     state="building",
        ...     type_="dynamic"
        ... )
        >>> print(f"Created segment: {response.name} (ID: {response.id})")
        Created segment: New Customers (ID: seg_123abc)
    
    Note:
        - This class inherits all fields and behavior from SegmentBaseModel
        - The response typically includes the segment's ID and initial state
    """

class GetSegmentResponse(SegmentBaseModel):
    """
    Response model for retrieving a specific segment in the Naxai People API.
    
    This class represents the response returned by the API when retrieving a single
    segment by its identifier. It inherits all fields from SegmentBaseModel.
    
    Example:
        >>> response = GetSegmentResponse(
        ...     id="seg_123abc",
        ...     name="Active US Customers",
        ...     description="Customers from the US who have been active in the last 30 days",
        ...     state="ready",
        ...     predefined=False,
        ...     type_="dynamic",
        ...     modified_at=1703066400000,
        ...     modified_by="usr_456def"
        ... )
        >>> print(f"Segment: {response.name} (State: {response.state})")
        Segment: Active US Customers (State: ready)
    
    Note:
        - This class inherits all fields and behavior from SegmentBaseModel
        - The response typically includes the complete segment definition and metadata
    """

class UpdateSegmentResponse(SegmentBaseModel):
    """
    Response model for segment updates in the Naxai People API.
    
    This class represents the response returned by the API when an existing segment
    is successfully updated. It inherits all fields from SegmentBaseModel.
    
    Example:
        >>> response = UpdateSegmentResponse(
        ...     id="seg_123abc",
        ...     name="Updated Segment Name",
        ...     description="Updated segment description",
        ...     state="building",
        ...     modified_at=1703066500000,
        ...     modified_by="usr_456def"
        ... )
        >>> print(f"Updated segment: {response.name} (State: {response.state})")
        Updated segment: Updated Segment Name (State: building)
    
    Note:
        - This class inherits all fields and behavior from SegmentBaseModel
        - The response typically includes the updated segment definition and metadata
        - The state may change to "building" if the segment needs to be recalculated
    """

class GetSegmentsHistoryResponse(BaseModel):
    """
    Response model for segment history in the Naxai People API.
    
    This class represents the response returned by the API when retrieving the
    historical membership data for a segment.
    
    Attributes:
        history (list[SegmentHistoryDay]): A list of daily history records for the segment.
    
    Example:
        >>> response = GetSegmentsHistoryResponse(
        ...     history=[
        ...         SegmentHistoryDay(date=1703066400000, added=25, removed=10, change=15, current=1250),
        ...         SegmentHistoryDay(date=1703152800000, added=18, removed=5, change=13, current=1263)
        ...     ]
        ... )
        >>> print(f"History entries: {len(response.history)}")
        >>> print(f"Current size: {response.history[-1].current}")
        History entries: 2
        Current size: 1263
    """
    history: list[SegmentHistoryDay]

class CountContactsInSegmentResponse(BaseModel):
    """
    Response model for counting contacts in a segment.
    
    This class represents the response returned by the API when requesting the
    number of contacts in a specific segment.
    
    Attributes:
        count (int): The number of contacts in the segment.
    
    Example:
        >>> response = CountContactsInSegmentResponse(count=1263)
        >>> print(f"The segment contains {response.count} contacts")
        The segment contains 1263 contacts
    """
    count: int

class GetSegmentUsageResponse(BaseModel):
    """
    Response model for segment usage information.
    
    This class represents the response returned by the API when retrieving information
    about where a segment is being used in campaigns and broadcasts.
    
    Attributes:
        campaign_ids (Optional[list[str]]): List of campaign IDs that use this segment.
        broadcast_ids (Optional[list[str]]): List of broadcast IDs that use this segment.
    
    Example:
        >>> response = GetSegmentUsageResponse(
        ...     campaignIds=["cmp_123", "cmp_456"],
        ...     broadcastIds=["brd_789"]
        ... )
        >>> print(f"Used in {len(response.campaign_ids)} campaigns and {len(response.broadcast_ids)} broadcasts")
        Used in 2 campaigns and 1 broadcasts
    
    Note:
        - This model supports both snake_case and camelCase field access
    """
    campaign_ids: Optional[list[str]] = Field(alias="campaignIds", default=None)
    broadcast_ids: Optional[list[str]] = Field(alias="broadcastIds", default=None)

    model_config = {"populate_by_name": True}

class ListContactsOfSegmentResponse(BaseModel):
    """
    Response model for retrieving contacts in a segment.
    
    This class represents the response returned by the API when retrieving the
    contacts that belong to a specific segment.
    
    Attributes:
        pagination (Pagination): Pagination information for the response.
        contacts (list[ContactBaseModel]): The list of contacts in the segment.
    
    Example:
        >>> response = ListContactsOfSegmentResponse(
        ...     pagination=Pagination(page=1, page_size=25, total_pages=5, total_items=123),
        ...     contacts=[
        ...         ContactBaseModel(nx_id="cnt_123", email="john@example.com"),
        ...         ContactBaseModel(nx_id="cnt_456", email="jane@example.com")
        ...     ]
        ... )
        >>> print(f"Page {response.pagination.page} of {response.pagination.total_pages}")
        >>> print(f"Showing {len(response.contacts)} of {response.pagination.total_items} contacts")
        Page 1 of 5
        Showing 2 of 123 contacts
    """
    pagination: Pagination
    contacts: list[ContactBaseModel]
