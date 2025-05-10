# django-extra-validators

A collection of extra validators for Django, including a strict `HTTPS URL` validator that checks:

- The URL starts with `https://`
- The target is reachable (HTTP 200 OK)
- The URL does **not** redirect (optional, strict mode)
- IBAN validator
- Dutch postal code validator

## Work in Progress

This package is a **work in progress**. I'm actively expanding it with validators commonly needed in real-world Django projects (e.g., URL shorteners, financial forms, address validation).

📬 **Suggestions and contributions are welcome!**  
If you have ideas for useful validators, feel free to open an issue or submit a PR.


## Features

- ✅ Enforce secure (`https://`) links
- ✅ Check URL reachability
- ✅ Prevent redirects for link integrity (e.g., in URL shorteners)
- ✅ Designed for use with Django models and forms
- ✅ Fully tested with `pytest` and `unittest.mock`

## Installation

```bash
pip install django-extra-validators
```

## Usage

### In a Django model

```python
from django.db import models
from django_extra_validators import validate_https_url

class Link(models.Model):
    url = models.URLField(validators=[validate_https_url])
```


### In a Django form
```python
from django import forms
from django_extra_validators import validate_https_url

class LinkForm(forms.Form):
    url = forms.URLField(validators=[validate_https_url])
```