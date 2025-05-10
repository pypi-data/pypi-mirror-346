from typing import Optional, Literal, Union
from pydantic import BaseModel, Field

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
    name: str
    operator: Literal["eq", "not-eq", "gt", "lt", "is-true", "is-false"]
    value: Optional[Union[str, int, bool]] = None

class EventProperties(BaseModel):
    all: Optional[list[EventPropertiesCondObject]]
    any: Optional[list[EventPropertiesCondObject]]

class EventObject(BaseModel):
    name: str
    count: int = Field(default=1)
    count_boundary: Literal["at-least", "at-most"] = Field(default="at-least", alias="countBoundary")
    time_boundary: Literal["all-time", "within-last", "before", "after"] = Field(default="all-time", alias="timeBoundary")
    period_boundary: Literal["day", "month"] = Field(default="day", alias="periodBoundary")
    interval_boundary: int = Field(default=1, alias="intervalBoundary", ge=1, le=366)
    date: Optional[int] = None
    properties: EventProperties

class AttributeArrayObject(BaseModel):
    operator: Literal["between", "is-timestamp-between"]
    field: str
    values: list = Field(min_length=2, max_length=2)

class AttributeObject(BaseModel):
    operator: CONDITIONS
    field: str
    value: Optional[Union[str, int, bool]]

class EventCond(BaseModel):
    event: EventObject = Field(default=None)

class AttributeCondArray(BaseModel):
    attribute: AttributeArrayObject = Field(default=None, min_length=1)

class AttributeCondSimple(BaseModel):
    attribute: AttributeObject = Field(default=None)

class AllCondGroup(BaseModel):
    all: list[Union[AttributeCondSimple, AttributeCondArray, EventCond]] = Field(min_length=1)

class AnyCondGroup(BaseModel):
    any: list[Union[AttributeCondSimple, AttributeCondArray, EventCond]] = Field(min_length=1)

class SearchCondition(BaseModel):
    all: Optional[list[Union[AttributeCondSimple, AttributeCondArray, EventCond, AllCondGroup, AnyCondGroup]]] = Field(default=None, min_length=1)
    any: Optional[list[Union[AttributeCondSimple, AttributeCondArray, EventCond, AllCondGroup, AnyCondGroup ]]] = Field(default=None, min_length=1)
