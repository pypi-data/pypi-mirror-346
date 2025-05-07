import json
from datetime import date, time, datetime
from enum import StrEnum


class IconType(StrEnum):
    AccessPoint = "AccessPoint"
    Alpha = "Alpha"
    Antenna = "Antenna"
    Bus = "Bus"
    Calendar = "Calendar"
    Car = "Car"
    Clipboard = "Clipboard"
    Clock = "Clock"
    Contacts = "Contacts"
    Conversation = "Conversation"
    CreditCard = "CreditCard"
    Document = "Document"
    Facebook = "Facebook"
    File = "File"
    Folder = "Folder"
    Group = "Group"
    Help = "Help"
    Home = "Home"
    Id = "Id"
    Image = "Image"
    InstantMessage = "InstantMessage"
    Location = "Location"
    Money = "Money"
    Notepad = "Notepad"
    Organization = "Organization"
    Person = "Person"
    Phone = "Phone"
    Phonebook = "Phonebook"
    Plane = "Plane"
    Train = "Train"

class PropertyValueType(StrEnum):
    BigInteger = "BigInteger"
    Boolean = "Boolean"
    Date = "Date"
    Double = "Double"
    Integer = "Integer"
    String = "String"
    Time = "Time"
    Timestamp = "Timestamp"

class AbstractPropertyValue(object):
    def __str__(self):
        return json.dumps(self.to_json(), indent=2)
    
    def to_json(self) -> dict:
        pass
    
    def from_json(self, json: dict):
        pass
    
    def get_property_value_type(self) -> PropertyValueType:
        pass

    def get_value(self) -> object:
        pass

class BigIntegerPropertyValue(AbstractPropertyValue):
    def __init__(self, value: int | None = None):
        self.value: int | None = value

    def to_json(self) -> dict:
        return {
            "property_value_type": PropertyValueType.BigInteger,
            "value": self.value,
        }

    def from_json(self, json: dict):
        self.value = json["value"]

    def get_property_value_type(self) -> PropertyValueType:
        return PropertyValueType.BigInteger

    def get_value(self) -> int:
        return self.value

class BooleanPropertyValue(AbstractPropertyValue):
    def __init__(self, value: bool | None = None):
        self.value: bool | None = value

    def to_json(self) -> dict:
        return {
            "property_value_type": PropertyValueType.Boolean,
            "value": self.value,
        }

    def from_json(self, json: dict):
        self.value = json["value"]

    def get_property_value_type(self) -> PropertyValueType:
        return PropertyValueType.Boolean

    def get_value(self) -> bool:
        return self.value

class DatePropertyValue(AbstractPropertyValue):
    def __init__(self, value: date | None = None):
        self.value: date | None = value

    def to_json(self) -> dict:
        return {
            "property_value_type": PropertyValueType.Date,
            "value": self.value.isoformat(),
        }

    def from_json(self, json: dict):
        self.value = date.fromisoformat(json["value"])

    def get_property_value_type(self) -> PropertyValueType:
        return PropertyValueType.Date

    def get_value(self) -> date:
        return self.value

class DoublePropertyValue(AbstractPropertyValue):
    def __init__(self, value: float | None = None):
        self.value: float | None = value

    def to_json(self) -> dict:
        return {
            "property_value_type": PropertyValueType.Double,
            "value": self.value,
        }

    def get_property_value_type(self) -> PropertyValueType:
        return PropertyValueType.Double

    def get_value(self) -> float:
        return self.value

class IntegerPropertyValue(AbstractPropertyValue):
    def __init__(self, value: int | None = None):
        self.value: int | None = value

    def to_json(self) -> dict:
        return {
            "property_value_type": PropertyValueType.Integer,
            "value": self.value,
        }
    
    def from_json(self, json: dict):
        self.value = json["value"]

    def get_property_value_type(self) -> PropertyValueType:
        return PropertyValueType.Integer

    def get_value(self) -> int:
        return self.value

class StringPropertyValue(AbstractPropertyValue):
    def __init__(self, value: str | None = None):
        self.value: str | None = value

    def to_json(self) -> dict:
        return {
            "property_value_type": PropertyValueType.String,
            "value": self.value,
        }
    
    def from_json(self, json: dict):
        self.value = json["value"]

    def get_property_value_type(self) -> PropertyValueType:
        return PropertyValueType.String

    def get_value(self) -> str:
        return self.value

class TimePropertyValue(AbstractPropertyValue):
    def __init__(self, value: time | None = None):
        self.value: time | None = value

    def to_json(self) -> dict:
        return {
            "property_value_type": PropertyValueType.Time,
            "value": self.value.isoformat(),
        }

    def from_json(self, json: dict):
        self.value = time.fromisoformat(json["value"])

    def get_property_value_type(self) -> PropertyValueType:
        return PropertyValueType.Time

    def get_value(self) -> time:
        return self.value

class TimestampPropertyValue(AbstractPropertyValue):
    def __init__(self, value: datetime | None = None):
        self.value: datetime | None = value

    def to_json(self) -> dict:
        return {
            "property_value_type": PropertyValueType.Timestamp,
            "value": self.value.isoformat(),
        }

    def from_json(self, json: dict):
        self.value = datetime.fromisoformat(json["value"])

    def get_property_value_type(self) -> PropertyValueType:
        return PropertyValueType.Timestamp

    def get_value(self) -> datetime:
        return self.value

def property_value_from_json(json: dict) -> AbstractPropertyValue:
    property_value: [AbstractPropertyValue | None] = None
    property_value_type: PropertyValueType = json["property_value_type"]
    match property_value_type:
        case PropertyValueType.BigInteger:
            property_value = BigIntegerPropertyValue()
        case PropertyValueType.Boolean:
            property_value = BooleanPropertyValue()
        case PropertyValueType.Date:
            property_value = DatePropertyValue()
        case PropertyValueType.Double:
            property_value = DoublePropertyValue()
        case PropertyValueType.Integer:
            property_value = IntegerPropertyValue()
        case PropertyValueType.String:
            property_value = StringPropertyValue()
        case PropertyValueType.Time:
            property_value = TimePropertyValue()
        case PropertyValueType.Timestamp:
            property_value = TimestampPropertyValue()
    property_value.from_json(json)
    return property_value
