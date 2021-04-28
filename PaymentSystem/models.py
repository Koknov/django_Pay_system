import uuid
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, username, password=None):
        if username is None:
            raise TypeError('Users must have a username.')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password):
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(username, password)
        user.save()

        return user


class Users(AbstractBaseUser):
    """
    Users model class

    Attributes:
        username            User's name
        password            User's password
        wallet_number       Unique wallet number, automatically generated
        total               Total amount of money

    """
    id = models.UUIDField(default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    wallet_number = models.CharField(max_length=36, unique=True, default=uuid.uuid4, primary_key=True)
    total = models.IntegerField(default=5000)
    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return "{} [{}] <{}> : {}".format(self.username, self.password, self.wallet_number, self.total)


class Transaction(models.Model):
    """
    Transaction model class

    Attributes:
        sender_wallet_number        Sender's wallet number
        receiver_wallet_number      Receiver's wallet number
        transaction_amount          Amount of money to send

    """

    sender_wallet_number = models.ForeignKey(Users, related_name='senders_wallet', on_delete=models.RESTRICT)
    receiver_wallet_number = models.ForeignKey(Users, related_name='receiver_wallet', on_delete=models.RESTRICT)
    transaction_amount = models.IntegerField()

    def __str__(self):
        return "from {} to {}: {}".format(self.sender_wallet_number, self.receiver_wallet_number,
                                          self.transaction_amount)
