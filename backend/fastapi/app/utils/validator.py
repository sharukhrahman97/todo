import re
from pydantic import ConstrainedStr

PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$"
)

class PasswordStr(ConstrainedStr):
    min_length = 8

    @classmethod
    def validate(cls, value):
        value = super().validate(value)
        if not PASSWORD_REGEX.match(value):
            raise ValueError(
                "Password must be at least 8 characters long, "
                "contain at least one uppercase letter, one lowercase letter, "
                "one number, and one special character."
            )
        return value
