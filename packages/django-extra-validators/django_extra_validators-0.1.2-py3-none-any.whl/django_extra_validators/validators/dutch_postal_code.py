import re

from django.core.exceptions import ValidationError


def validate_dutch_postal_code(value: str) -> None:
    """
    Validate Dutch postal codes.

    A valid Dutch postal code consists of four digits followed by a space and two uppercase letters.
    For example: 1234 AB.

    :param value: The postal code to validate.
    :raises ValidationError: If the postal code is invalid.
    """
    if not re.match(r'^\d{4}\s?[A-Z]{2}$', value):
        raise ValidationError(
            "Enter a valid Dutch postal code (e.g. 1234 AB).",
            code='invalid_postal_code',
        )
