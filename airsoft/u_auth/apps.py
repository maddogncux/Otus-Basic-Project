# pylint: disable=too-many-ancestors
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from django.apps import AppConfig


class UAuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "u_auth"
