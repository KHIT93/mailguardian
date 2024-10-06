# django.contrib.auth.password_validation.UserAttributeSimilarityValidator
# django.contrib.auth.password_validation.MinimumLengthValidator
# django.contrib.auth.password_validation.CommonPasswordValidator
# django.contrib.auth.password_validation.NumericPasswordValidator

from difflib import SequenceMatcher
import re
from pathlib import Path

class BaseValidator:
    def validate(self, password: str, user = None) -> None:
        raise NotImplementedError()
    
    def get_help_text(self) -> str:
        raise NotImplementedError()


class MinimumLengthValidator(BaseValidator):
    """
    Validate that the password is of a minimum length.
    """

    def __init__(self, min_length=4):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValueError(
                "This password is too short. It must contain at least "
                "%(min_length)d character."  % {"min_length": self.min_length}
            )

    def get_help_text(self):
        return "Your password must contain at least %(min_length)d character." % {"min_length": self.min_length}
    
def exceeds_maximum_length_ratio(password, max_similarity, value):
    """
    Test that value is within a reasonable range of password.

    The following ratio calculations are based on testing SequenceMatcher like
    this:

    for i in range(0,6):
      print(10**i, SequenceMatcher(a='A', b='A'*(10**i)).quick_ratio())

    which yields:

    1 1.0
    10 0.18181818181818182
    100 0.019801980198019802
    1000 0.001998001998001998
    10000 0.00019998000199980003
    100000 1.999980000199998e-05

    This means a length_ratio of 10 should never yield a similarity higher than
    0.2, for 100 this is down to 0.02 and for 1000 it is 0.002. This can be
    calculated via 2 / length_ratio. As a result we avoid the potentially
    expensive sequence matching.
    """
    pwd_len = len(password)
    length_bound_similarity = max_similarity / 2 * pwd_len
    value_len = len(value)
    return pwd_len >= 10 * value_len and value_len < length_bound_similarity
    
class UserAttributeSimilarityValidator(BaseValidator):
    """
    Validate that the password is sufficiently different from the user's
    attributes.

    If no specific attributes are provided, look at a sensible list of
    defaults. Attributes that don't exist are ignored. Comparison is made to
    not only the full attribute value, but also its components, so that, for
    example, a password is validated against either part of an email address,
    as well as the full address.
    """

    DEFAULT_USER_ATTRIBUTES = ("first_name", "last_name", "email")

    def __init__(self, user_attributes=DEFAULT_USER_ATTRIBUTES, max_similarity=0.7):
        self.user_attributes = user_attributes
        if max_similarity < 0.1:
            raise ValueError("max_similarity must be at least 0.1")
        self.max_similarity = max_similarity

    def validate(self, password, user=None):
        if not user:
            return

        password = password.lower()
        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_lower = value.lower()
            value_parts = re.split(r"\W+", value_lower) + [value_lower]
            for value_part in value_parts:
                if exceeds_maximum_length_ratio(password, self.max_similarity, value_part):
                    continue
                if (SequenceMatcher(a=password, b=value_part).quick_ratio() >= self.max_similarity):
                    raise ValueError(
                        "The password is too similar to the %(name)s." % {"name": attribute_name}
                    )

    def get_help_text(self):
        return "Your password can not be too similar to your other personal information."
    
class NumericPasswordValidator(BaseValidator):
    """
    Validate that the password is not entirely numeric.
    """

    def validate(self, password, user=None):
        if password.isdigit():
            raise ValueError(
                "This password is entirely numeric."
            )

    def get_help_text(self):
        return "Your password can’t be entirely numeric."
    
class CommonPasswordValidator(BaseValidator):
    """
    Validate that the password is not a common password.

    The password is rejected if it occurs in a provided list of passwords,
    By default, we use this list:
    https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt
    """

    @property
    def DEFAULT_PASSWORD_LIST_PATH(self):
        return Path(__file__).resolve().parent / "common-passwords.txt"

    def __init__(self, password_list_path: Path = DEFAULT_PASSWORD_LIST_PATH):
        if password_list_path is CommonPasswordValidator.DEFAULT_PASSWORD_LIST_PATH:
            password_list_path = self.DEFAULT_PASSWORD_LIST_PATH
        
        with password_list_path.open("r", encoding="utf-8") as f:
            self.passwords = {x.strip() for x in f.readlines()}

    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValueError(
                "This password is too common."
            )

    def get_help_text(self):
        return "Your password can not be a commonly used password."