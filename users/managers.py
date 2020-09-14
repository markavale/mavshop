# from django.contrib.auth.models import BaseUserManager
# from django.db.models import Q
# from django.db import models


# class UserManager(BaseUserManager):
#     def create_user(self, username, first_name, middle_name, last_name, password=None, is_active=True, is_staff=False,
#                     is_admin=False):
#         if not username:
#             raise ValueError("Users must have a username")
#         if not first_name:
#             raise ValueError("Users must have a first name")
#         if not middle_name:
#             raise ValueError("Users must have a middle name")
#         if not last_name:
#             raise ValueError("Users must have a last name")
#         if not password:
#             raise ValueError("Users must have a password")
#         user = self.model(
#             username=username,
#             first_name=first_name,
#             middle_name=middle_name,
#             last_name=last_name
#         )
#         user.set_password(password)  # change user password
#         user.staff = is_staff
#         user.admin = is_admin
#         user.active = is_active
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, first_name, last_name, username, email, password, is_staff=True, is_admin=True):
#         user = self.model(
#             username=username,
#             first_name=first_name,
#             last_name=last_name,
#             email=email
#         )
#         user.admin = is_admin
#         user.staff = is_staff
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
