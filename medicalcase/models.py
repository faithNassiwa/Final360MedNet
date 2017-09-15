import datetime
from django.db import models
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from userprofile.models import Doctor
from autoslug import AutoSlugField
from multiselectfield import MultiSelectField


GENDER = (('Female', 'Female'), ('Male', 'Male'), ('Others', 'Others'))

PURPOSE = (('I need help to arrive at diagnosis', 'I need help to arrive at diagnosis'),
           ('Interesting case, a lot to learn', 'Interesting case, a lot to learn'),
           ('Rare case', 'Rare case'), ('Personal write up to improve skill', 'Personal write up to improve skill'))


class MedicalCaseCategory(models.Model):
    name = models.CharField(max_length=200, blank=False, default="General Medicine ")
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Medical Case Categories"

    def __str__(self):
        return self.name


class MedicalCase(models.Model):
    title = models.CharField(max_length=200)
    chief_complaint = models.CharField(max_length=200)
    purpose = MultiSelectField(choices=PURPOSE, verbose_name="Reason for sharing medical case")
    patient_age = models.CharField(max_length=200)
    patient_gender = models.CharField(max_length=6, choices=GENDER, default='Female')
    patient_country_of_origin = models.CharField(max_length=200)
    history_of_present_illness = models.TextField()
    medical_history = models.TextField()
    surgical_history = models.TextField()
    social_history = models.TextField()
    family_history = models.TextField()
    allergies = models.TextField()
    medications = models.TextField()
    review_of_systems = models.TextField()
    physical_examination = models.TextField()
    diagnostic_tests = models.TextField()
    medical_case_category = models.ManyToManyField(MedicalCaseCategory)
    any_other_details = models.TextField()
    #slug = AutoSlugField(null=True, default=None, unique=True, populate_from='title', unique_with='created_at')
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    doctor = models.ForeignKey(Doctor, models.DO_NOTHING, blank=False, null=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Medical Cases"

    @classmethod
    def list_medical_cases(cls):
        return cls.objects.all()

    @classmethod
    def weekly_top_five_medical_case(cls):
        date_diff = datetime.datetime.now() - datetime.timedelta(days=7)
        return cls.objects.filter(created_at__range=(date_diff, datetime.datetime.now())).order_by('-created_at')[:5]

    @classmethod
    def send_medical_cases(cls, subject_medical_case, context, registered_doctor):
        subject = subject_medical_case.title
        message = render_to_string('medicalcase/emails/medical_case_email_update.html', context)
        to_email1 = registered_doctor.user.email
        email = EmailMessage(subject, message, to=[to_email1])
        email.content_subtype = "html"
        email.send()


class Photo(models.Model):
    diagnotic_image = models.ImageField(upload_to="medical_cases", height_field=None, width_field=None, blank=True, null=True)
    medical_case = models.ForeignKey(MedicalCase)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Photos"


class Comment(models.Model):
    comment_content = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    medical_case = models.ForeignKey(MedicalCase)
    doctor = models.ForeignKey(Doctor, related_name="doctor_comments")

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Comments"


class Reply(models.Model):
    reply_content = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    parent_comment_id = models.ForeignKey(Comment)
    medical_case = models.ForeignKey(MedicalCase)
    doctor = models.ForeignKey(Doctor, related_name="doctor_replies")

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Replies"

