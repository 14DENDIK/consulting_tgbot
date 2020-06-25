from django.db import models
from django.utils.translation import gettext as _

STEP_CHOICES = (
    ('main_menu', _('Main page')),
    ('faqs', _('FAQs')),
    ('about', _('About')),
    ('countries_list', _('Counties List')),
    ('application_name', _('Application Name')),
    ('application_contact', _('Application Contact')),
    ('application_visa_type', _('Application visa type'))
)

VISA_TYPES = (
    ('student_visa', _('Student visa')),
    ('tourist_visa', _('Tourist visa')),
    ('work_visa', _('Work visa')),
    ('business_visa', _('Business visa')),
    ('guest_visa', _('Guest visa')),
    ('pr_visa', _('PR visa')),

)


class TelegramUser(models.Model):
    user_id = models.CharField(max_length=50)
    full_username = models.CharField(max_length=255, null=True, blank=True)
    phone_num = models.CharField(max_length=20, null=True, blank=True)
    step = models.CharField(
        choices=STEP_CHOICES,
        max_length=255,
        default='main_menu'
    )
    full_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user_id + " " + self.full_username


class Country(models.Model):
    name = models.CharField(max_length=255)
    docs = models.FileField(upload_to="pdf-docs/")

    def __str__(self):
        return self.name


class Application(models.Model):
    client = models.CharField(max_length=255, null=True, blank=True)
    phone_num = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    visa_type = models.CharField(choices=VISA_TYPES, max_length=255, default='student_visa')

    def __str__(self):
        return self.client + " " + self.visa_type + " " + self.phone_num


class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()

    def __str__(self):
        return self.question
