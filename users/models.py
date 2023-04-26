from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.db.models import TextChoices
# Create your models here.


class TemplateChoices(TextChoices):
    TEMPLATE_1 = 1
    TEMPLATE_2 = 2


class User(AbstractUser):
    email = models.EmailField(null=True,blank=True,unique=True)
    username = models.CharField(max_length=300,null=True , blank=True)
    password = models.CharField(max_length=1000 , null=True , blank=True)
    institute = models.CharField(max_length=1000,null=True,blank=True)
    phone = models.DateTimeField(null=True,blank=True)

    REQUIRED_FIELDS = []

    USERNAME_FIELD = 'email'

    login_token = models.TextField(null=True, blank=True)
    last_login = models.DateTimeField(null=True,blank=True)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.email


class UserTemplate(models.Model):
    template_type = models.CharField(max_length=2000, null=True, blank=True, choices=TemplateChoices.choices,
                                     default=TemplateChoices.TEMPLATE_1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_template")

    def __str__(self):
        return self.email
