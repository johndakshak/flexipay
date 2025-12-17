from enum import Enum

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"

class UserRole(Enum):
    USER = "user"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"