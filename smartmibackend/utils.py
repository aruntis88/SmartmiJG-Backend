from django.core.validators import RegexValidator


phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                             message="Phone number must be entered in the format: '9999999999'. Up to 10 digits allowed.")
