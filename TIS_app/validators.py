from django.core.exceptions import ValidationError


def validate_password(value):
    if value.isdigit():
        raise ValidationError("Password cannot contain only numbers !")
    if value.islower():
        raise ValidationError("Password must contain one uppercase letter !")
    if value.isupper():
        raise ValidationError("Password must contain one lowercase letter !")
    if value.find(" ") != -1:
        raise ValidationError("Password cannot contain  whitespace !")
    if value.isalpha():
        raise ValidationError("Password must contain one digit and one special character !")
    if len(value) < 9:
        raise ValidationError("Password must be longer than 8 characters !")
