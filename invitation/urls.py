from django.conf.urls import url
from invitation import views as invitation_views
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm1, RegistrationForm2, RegistrationForm3

urlpatterns = [
    url(r'^invite/$', invitation_views.invite_user, name='invite'),
    url(r'^bulk/invite/$', invitation_views.bulk_invite, name='bulk-invite'),
    url(r'^friend/invite/$', login_required(invitation_views.invite_friend), name='friend_invite'),
    url(r'^join/(?P<code>[a-zA-Z0-9]+)/$', invitation_views.join, name='join'),
    url(r'^join/friend/(?P<code>[a-zA-Z0-9]+)/$', invitation_views.join_friend_invite, name='join_friend_invite'),
    url(r'^register_medic/$', invitation_views.register_invited_user, name='register_invited_user'),
    url(r'^signup/1/$', invitation_views.registration_one, name='reg_1'),
    url(r'^signup/2/$', invitation_views.registration_two, name='reg_2'),
    url(r'^signup/complete/$', invitation_views.done, name='finished'),
    url(r'^suggest/health-professional/$', invitation_views.send_suggested_invitee, name='suggest-doctor'),
    url(r'^invite_email/$', invitation_views.invite_email),
    url(r'^sign_up_email/$', invitation_views.sign_up),
    url(r'^thank_you_signup_email/$', invitation_views.thank_you_signup),
]
