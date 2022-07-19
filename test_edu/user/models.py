from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """Creates and saves a User with the given email and password."""
        if not email:
            raise ValueError("Users must have an email address")
       

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, password=None
    ):
        """Creates and saves a superuser with the given email and password."""
        user = self.create_user(
            email, password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        _("Email"),
        unique=True,
        max_length=256,
        null=False,
        blank=False,
    )
    is_active = models.BooleanField(
        _("Is Active"),
        default=True,
    )
    is_staff = models.BooleanField(
        _("Is Staff"),
        default=False,
    )
    is_superuser = models.BooleanField(
        _("Is Superuser"),
        default=False,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:

        verbose_name_plural = "Users"


    def __str__(self) -> str:
        return f"<User ({self.id}) {self.email}>"

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True
