from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# No need to create a custom User model as the requirements can be met with Django's default User model
# The User class in the UML diagram maps to Django's User model with username and password fields

# For the Admin class that inherits from User, we'll use Django's admin permissions system
# An admin will be a User with is_staff=True