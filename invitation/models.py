from django.db import models
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class Invitation(models.Model):
    name = models.CharField(max_length=100)
    organization = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    code = models.CharField(max_length=6)
    accepted = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name

    def send_invite(self):
        subject = 'Invitation to join 360MedNet'
        link = 'http://%s/join/%s/' % (
            settings.SITE_HOST,
            self.code
        )
        website = 'http://%s/' % (
            settings.SITE_HOST,

        )
        context = Context({
            'name': self.name,
            'organization': self.organization,
            'link': link,
            'website': website,
            'code': self.code
        })

        html_content = render_to_string('invitation/invitation_email.html', context)
        text_content = strip_tags(html_content)

        message = html_content
        msg = EmailMultiAlternatives(
            subject, message,
            settings.EMAIL_HOST_USER, [self.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


class FriendInvitation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    code = models.CharField(max_length=20)
    accepted = models.BooleanField(default=False)
    sender = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name

    def send_invite(self):
        subject = 'Invitation to join 360MedNet'
        link = 'http://%s/join/friend/%s/' % (
            settings.SITE_HOST,
            self.code
        )
        template = get_template('invitation/friend_invitation_email.html')
        context = Context({
            'name': self.name,
            'sender': self.sender,
            'link': link,
        })
        message = template.render(context)
        msg = send_mail(
            subject, message,
            settings.EMAIL_HOST_USER, [self.email]
        )
        msg.attach_alternative(message, "text/html")
        msg.send()


class SuggestedInvitee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    invitation_status = models.BooleanField(default=False)
    verification_status = models.BooleanField(default=False)
    doctor = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, auto_now_add=False)


class Image(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="emails", blank=True, null=True)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, auto_now_add=False)