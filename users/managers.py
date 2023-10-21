from django.contrib.auth.models import (
    BaseUserManager
)


class UserManager(BaseUserManager):

    def create_user(self, phone, birth_date, profile_pic=None, first_name=None, password=None):
        if phone is None:
            raise TypeError('Users must have a phone.')

        user = self.model(phone=phone)
        user.set_password(password)
        user.first_name = first_name
        user.birth_date = birth_date
        user.profile_pic = profile_pic
        user.save()

        return user

    def create_superuser(self, phone, birth_date=None, profile_pic=None, first_name=None, password=None):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(phone=phone, birth_date=birth_date, profile_pic=profile_pic, first_name=first_name, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
