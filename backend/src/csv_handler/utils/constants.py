from enum import Enum

class ServiceType(Enum):
    New = "New"
    Change = "Change"
    Variation = "Variation"
    Cancellation = "Cancellation"



ACCEPTED_APPLICATION_TYPES = [
    ServiceType.New.value,
    ServiceType.Cancellation.value,
    ServiceType.Change.value,
    ServiceType.Variation.value
]