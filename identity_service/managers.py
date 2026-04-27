import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _get_default_organization(self):
        organization_model = self.model._meta.get_field("organization").related_model
        organization, _ = organization_model._default_manager.db_manager(self._db).get_or_create(
            name="System Administration"
        )
        return organization

    def _create_user(self, email: str, password: str, **extra_fields):
        if not email:
            raise ValueError("The email field must be set.")
        if not password:
            raise ValueError("Password must be set.")
        if not extra_fields.get("organization"):
            raise ValueError("Users must be assigned to an organization.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields):
        if not password:
            raise ValueError("Superusers must have a password.")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("organization", self._get_default_organization())

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        with transaction.atomic(using=self._db):
            return self._create_user(email, password, **extra_fields)