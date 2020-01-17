import jwt
from datetime import datetime, timedelta
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, phone, name, password=None):
        if email is None:
            raise ValueError('Email is required')
        user = self.model(email=self.normalize_email(email),
                          name=name,
                          phone=phone)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, phone, name, password=None):
        if email is None:
            raise ValueError('Email is required')
        user = self.model(user=self.normalize_email(email),
                          name=name,
                          phone=phone)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=155, unique=True)
    phone = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=25)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'name']

    objects = UserManager()

    def get_full_name(self):
        return self.name

    def get_username(self):
        return self.email

    @property
    def token(self):
        dt = datetime.now() + timedelta(days=60)
        payload = {
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }

        jwt_token = jwt.encode(payload, 'pradator', algorithm='HS256')

        return jwt_token.decode('utf-8')

    @property
    def is_staff(self):
        return self.is_admin
