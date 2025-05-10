import re

import requests
from django.core.exceptions import ValidationError


def validate_https_url(value: str) -> None:
    if not re.match(r'^https://', value):
        raise ValidationError(
            "Enter a valid HTTPS URL (e.g. https://example.com).",
            code='invalid_https_url',
        )

    try:
        response = requests.get(value, allow_redirects=True)

        if response.history:
            raise ValidationError(
                "The URL was redirected, please provide a direct URL.",
                code='redirected_url',
            )

        if response.status_code != 200:
            raise ValidationError(
                "The URL is not reachable.",
                code='unreachable_url',
            )
    except requests.RequestException:
        raise ValidationError(
            "The URL is not reachable.",
            code='unreachable_url',
        )
