import re

import dns.resolver
from django.core.validators import ValidationError


def _check_mailadres_extract_domain(email: str) -> str:
    try:
        local, domain = email.split('@')
    except ValueError:
        raise ValidationError('Email address is not valid')

    return domain


def validate_email(value: str) -> None:
    domain = _check_mailadres_extract_domain(value)
    try:
        dns.resolver.resolve(domain, 'MX')

    except dns.resolver.NoAnswer:
        raise ValidationError(
            "The domain does not have a valid MX record.",
            code='invalid_email_domain',
        )
    except dns.resolver.NXDOMAIN:
        raise ValidationError(
            "The domain does not exist.",
            code='non_existent_domain',
        )
    except dns.resolver.Timeout:
        raise ValidationError(
            "The DNS query timed out.",
            code='dns_timeout',
        )
    except dns.resolver.NoNameservers:
        raise ValidationError(
            "No nameservers found for the domain.",
            code='no_nameservers',
        )
    except dns.exception.DNSException:
        raise ValidationError(
            "An error occurred while resolving the domain.",
            code='dns_error',
        )
    except Exception as e:
        raise ValidationError(
            f"An unexpected error occurred: {str(e)}",
            code='unexpected_error',
        )
