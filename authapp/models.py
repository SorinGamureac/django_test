from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.timezone import now

from geekshop import settings
from geekshop.settings import USER_EXPIRES_TIMEDELTA


def get_activation_key_expires():
    return now() + USER_EXPIRES_TIMEDELTA

class ShopUser(AbstractUser):
    age = models.PositiveSmallIntegerField(verbose_name='возраст', null=True)
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(
        default=get_activation_key_expires
    )

    def is_activation_key_expired(self):
        return now() > self.activation_key_expires

    def send_verify_mail(self):
        verify_link = reverse(
            'auth:user_verify',
            kwargs={
                'email': self.email,
                'activation_key': self.activation_key
            }
        )

        title = f'Подтверждение учетной записи {self.username}'

        message = f'Для подтверждения учетной записи {self.username} на портале ' \
                  f'{settings.DOMAIN_NAME} перейдите по ссылке: \n' \
                  f'{settings.DOMAIN_NAME}{verify_link}'

        return self.email_user(
            title, message, settings.EMAIL_HOST_USER, fail_silently=False
        )
        # return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    class Meta:
        ordering = ['-is_active', '-is_superuser', '-is_staff', 'username']

    @cached_property
    def basket_items(self):
        return self.basketitem_set.all()

    def basket_cost(self):
        return sum(item.product.price * item.quantity for item in self.basket_items)

    def basket_total_quantity(self):
        return sum(item.quantity for item in self.basket_items)

class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'мужской'),
        (FEMALE, 'женский'),
    )

    user = models.OneToOneField(ShopUser, primary_key=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='теги', max_length=128, blank=True)
    aboutMe = models.TextField(verbose_name='о себе', max_length=512, blank=True)
    gender = models.CharField(verbose_name='пол', max_length=1,
                              choices=GENDER_CHOICES, blank=True)