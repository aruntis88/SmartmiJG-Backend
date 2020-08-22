from django.db import models
from django.contrib.auth.models import AbstractUser

# from address.models import AddressField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from applications.common.models import Company
from applications.users.managers import CustomUserManager, UserQueryset
from smartmibackend.utils import phone_regex


class User(AbstractUser):
    ROLES = (
        ('A', 'Admin'),
        ('S', 'Sales'),
    )
    DESIGNATIONS = (
        ('SE', 'Sales Engineer'),
        ('SO', 'Software Engineer'),
    )
    DEPARTMENTS = (
        ('A', 'Administration'),
        ('S', 'Sales'),
    )
    employee_code = models.CharField(max_length=25, blank=True)
    designation = models.CharField(max_length=2, choices=DESIGNATIONS, default='SE')
    role = models.CharField(max_length=2, choices=ROLES, default='S')
    company = models.ForeignKey(Company, related_name='user_company', on_delete=models.PROTECT, blank=True, null=True)
    department = models.CharField(max_length=2, choices=ROLES, default='S')
    reporting = models.ForeignKey("self", related_name='user_reports', on_delete=models.PROTECT, blank=True, null=True) # mandatory
    telephone = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    # phone = models.CharField(validators=[phone_regex], max_length=10, blank=True, null=True)
    photo = models.ImageField(upload_to='users/', default='img/users/no-img.jpg', blank=True, null=True)
    assigned_companies = models.ManyToManyField(Company, related_name='user_assigned_companies', blank=True)

    objects = CustomUserManager()
    query_objects = UserQueryset.as_manager()

    def __str__(self):
        return str(self.first_name)

    class Meta:
        ordering = ['-id']


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# from django.db.models import Q
#
# from django.contrib.auth import get_user_model
#
# MyUser = get_user_model()
#
#
# class UsernameOrEmailBackend(object):
#     def authenticate(self, username=None, password=None, **kwargs):
#         try:
#            # Try to fetch the user by searching the username or email field
#             user = MyUser.objects.get(Q(username=username)|Q(email=username))
#             if user.check_password(password):
#                 return user
#         except MyUser.DoesNotExist:
#             # Run the default password hasher once to reduce the timing
#             # difference between an existing and a non-existing user (#20760).
#             MyUser().set_password(password)



