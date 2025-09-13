from django.core.validators import RegexValidator
from common.utils.messages import message as _

"""Validateurs personnalisés pour les champs de formulaire."""

username_validator = RegexValidator(regex=r"^[a-zA-Z0-9_]+$", message=_("ERROR_USERNAME_INVALID"))
password_validator = RegexValidator(
    regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d\s])[^\s]{8,}$",
    message=_("ERROR_PASSWORD_INVALID")
)
email_validator = RegexValidator(
    regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|org|net|edu|gov|mil|biz|info|io|co|fr)$",
    message=_("ERROR_EMAIL_INVALID")
)
name_validator = RegexValidator(
    regex=r"^[a-zA-ZÀ-ÿ '-]+$",
    message=_("ERROR_NAME_INVALID")
)
