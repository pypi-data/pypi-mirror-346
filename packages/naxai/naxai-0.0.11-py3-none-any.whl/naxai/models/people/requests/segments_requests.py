from pydantic import BaseModel, Field
from typing import Optional, Literal, Union

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
    when creating segments based on event data.
    
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
    when creating segments. It supports both "all" (AND) and "any" (OR) logical
    combinations of conditions.
    
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
    used when creating segments.
    
    Attributes:
        name (str): The name of the event to evaluate.
        count (int): The number of times the event should have occurred. Defaults to 1.
        count_boundary (Literal): Whether the count should be at least or at most the specified value.
            Must be either "at-least" or "at-most". Defaults to "at-least".
            Mapped from JSON key 'countBoundary'.
        time_boundary (Literal): The time frame to consider for the events.
            Must be one of "all-time", "within-last", "before", "after". Defaults to "all-time".
            Mapped from JSON key 'timeBoundary'.
        period_boundary (Literal): The unit of time for time_boundary.
            Must be either "day" or "month". Defaults to "day".
            Mapped from JSON key 'periodBoundary'.
        interval_boundary (int): The number of time units for time_boundary.
            Must be between 1 and 366. Defaults to 1.
            Mapped from JSON key 'intervalBoundary'.
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
    used when creating segments.
    
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
    attribute: AttributeArrayObject = Field(default=None, min_length=1)

class AttributeCondSimple(BaseModel):
    """
    Model representing a simple attribute condition wrapper in segment definitions.
    
    This class serves as a wrapper for AttributeObject instances to be used in
    condition groups within segment definitions.
    
    Attributes:
        attribute (AttributeObject): The attribute condition to apply.
    
    Example:
        >>> # Create a simple attribute condition for country equals "US"
        >>> attr_obj = AttributeObject(
        ...     operator="eq",
        ...     field="country",
        ...     value="US"
        ... )
        >>> condition = AttributeCondSimple(attribute=attr_obj)
    """
    attribute: AttributeObject = Field(default=None, min_length=1)

class AllCondGroup(BaseModel):
    """
    Model representing a group of conditions joined by logical AND.
    
    This class combines multiple conditions where all must be satisfied for a contact
    to be included in a segment.
    
    Attributes:
        all (list[Union[AttributeCondSimple, AttributeCondArray, EventCond]]): 
            List of conditions that must all be satisfied (AND logic).
    
    Example:
        >>> # Create a condition group where country is "US" AND has made a purchase
        >>> all_group = AllCondGroup(
        ...     all=[
        ...         AttributeCondSimple(attribute=AttributeObject(operator="eq", field="country", value="US")),
        ...         EventCond(event=EventObject(name="purchase", properties=EventProperties(all=[])))
        ...     ]
        ... )
    """
    all: list[Union[AttributeCondSimple, AttributeCondArray, EventCond]] = Field(min_length=1)

class AnyCondGroup(BaseModel):
    """
    Model representing a group of conditions joined by logical OR.
    
    This class combines multiple conditions where at least one must be satisfied for a
    contact to be included in a segment.
    
    Attributes:
        any (list[Union[AttributeCondSimple, AttributeCondArray, EventCond]]): 
            List of conditions where at least one must be satisfied (OR logic).
    
    Example:
        >>> # Create a condition group where country is either "US" OR "Canada"
        >>> any_group = AnyCondGroup(
        ...     any=[
        ...         AttributeCondSimple(attribute=AttributeObject(operator="eq", field="country", value="US")),
        ...         AttributeCondSimple(attribute=AttributeObject(operator="eq", field="country", value="Canada"))
        ...     ]
        ... )
    """
    any: list[Union[AttributeCondSimple, AttributeCondArray, EventCond]] = Field(min_length=1)

class Condition(BaseModel):
    """
    Model representing the top-level condition structure for segment definitions.
    
    This class defines the complete set of conditions for a segment, allowing for
    complex combinations of attribute and event conditions using logical AND/OR operations.
    
    Attributes:
        all (Optional[list]): List of conditions that must all be satisfied (AND logic).
            Can include simple conditions or nested condition groups.
        any (Optional[list]): List of conditions where at least one must be satisfied
            (OR logic). Can include simple conditions or nested condition groups.
    
    Example:
        >>> # Create a condition for active users who are from either US or Canada
        >>> condition = Condition(
        ...     all=[
        ...         AttributeCondSimple(attribute=AttributeObject(operator="eq", field="status", value="active")),
        ...         AnyCondGroup(
        ...             any=[
        ...                 AttributeCondSimple(attribute=AttributeObject(operator="eq", field="country", value="US")),
        ...                 AttributeCondSimple(attribute=AttributeObject(operator="eq", field="country", value="Canada"))
        ...             ]
        ...         )
        ...     ]
        ... )
    """
    all: Optional[list[Union[AttributeCondSimple, AttributeCondArray, EventCond, AllCondGroup, AnyCondGroup]]] = Field(default=None, min_length=1)
    any: Optional[list[Union[AttributeCondSimple, AttributeCondArray, EventCond, AllCondGroup, AnyCondGroup ]]] = Field(default=None, min_length=1)

class CreateSegmentRequest(BaseModel):
    """
    Request model for creating a new segment in the Naxai People API.
    
    This class defines the structure for segment creation requests, providing
    all the necessary fields to specify a segment's name, description, conditions,
    and type.
    
    Attributes:
        name (str): The name of the segment to create.
        description (Optional[str]): A description of the segment's purpose or criteria.
            Defaults to None.
        condition (Optional[Condition]): The conditions that define which contacts
            should be included in this segment. Required for dynamic segments.
            Defaults to None.
        type_ (Literal["manual", "dynamic"]): The type of segment to create.
            - "manual": Explicitly defined members that you'll add manually
            - "dynamic": Rule-based segment where members are determined by conditions
            Mapped from JSON key 'type'. Defaults to "manual".
    
    Example:
        >>> # Create a dynamic segment for active US customers
        >>> request = CreateSegmentRequest(
        ...     name="Active US Customers",
        ...     description="Customers from the US who have been active in the last 30 days",
        ...     type="dynamic",
        ...     condition=Condition(
        ...         all=[
        ...             AttributeCondSimple(attribute=AttributeObject(operator="eq", field="country", value="US")),
        ...             EventCond(
        ...                 event=EventObject(
        ...                     name="login",
        ...                     time_boundary="within-last",
        ...                     period_boundary="day",
        ...                     interval_boundary=30,
        ...                     properties=EventProperties(all=[])
        ...                 )
        ...             )
        ...         ]
        ...     )
        ... )
    
    Note:
        - For manual segments, the condition field is optional
        - For dynamic segments, the condition field is required
        - This model supports both snake_case and camelCase field access through populate_by_name
    """
    name: str
    description: Optional[str] = None
    condition: Optional[Condition] = None
    type_: Literal["manual", "dynamic"] = Field(default="manual", alias="type")

    class Config:
        populate_by_name = True

