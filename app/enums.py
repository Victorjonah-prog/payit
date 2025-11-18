from enum import Enum

class Gender(Enum):
    MALE = "male"
    FEMALE= "female"


class UserCategory(Enum):
    BUYER = "buyer"
    FARMER = "farmer"
    