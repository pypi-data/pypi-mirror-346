from schwifty import IBAN
from django.core.exceptions import ValidationError

def validate_iban(value: str) -> None:
    try:
        iban = IBAN(value)
        iban.validate()
    except ValueError:
        raise ValidationError(
            "Enter a valid IBAN (e.g. NL18RABO0123459876.",
            code='invalid_iban',
        )
