from schwifty import IBAN
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_iban(value: str) -> None:
    try:
        iban = IBAN(value)
        iban.validate()
    except ValueError:
        raise ValidationError(
            _("Enter a valid IBAN (e.g. NL18RABO0123459876."),
            code='invalid_iban',
        )
