from django.conf.urls import url
from django.contrib.auth import views as auth_views
from userprofile import views as user_views
from .views import EmailAuthenticationForm
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^login/$', auth_views.login, name='login', kwargs={'redirect_authenticated_user': True,
                                                             'template_name': 'userprofile/login.html',
                                                             'authentication_form': EmailAuthenticationForm,
                                                             'redirect_field_name': 'post',
                                                             }),
    url(r'^join/$', user_views.signup, name='join'),
    #url(r'^signup/email/activate/$', user_views.signup_activate, name='signup_activate'),
    url(r'^accounts/verified_registration/(?P<reg_number>[a-zA-Z0-9]+)/$', user_views.register, name='register'),
    url(r'^accounts/unverified_registration/$', user_views.unverified_register, name='unverified_register'),
    url(r'^$', user_views.verify, name='verify'),
    url(r'^medic/(?P<username>[\w.@+-]+)/$', user_views.get_profile, name='profile'),
    url(r'^update/(?P<pk>[\-\w]+)/$', login_required(user_views.UpdateProfile.as_view()), name='update_doctor'),
    url(r'^complete/registration/(?P<pk>[\-\w]+)/$', user_views.RegisterUpdateView.as_view(),
        name='update_registration'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^(?P<pk>[0-9]+)/detail/$', login_required(user_views.DoctorDetail.as_view()),
        name='doctor-detail'),
    url(r'^home/$', user_views.home, name='home'),
    url(r'^add/qualification/$', login_required(user_views.QualificationCreate.as_view()), name='add_qualification'),
    url(r'^medic/qualification/details/(?P<pk>[0-9]+)/$', login_required(user_views.QualificationDetail.as_view()),
        name='qualification-detail'),
    url(r'^password-reset/$', auth_views.password_reset, name='password_reset',
        kwargs={'template_name': 'userprofile/password_reset_form.html',
                'email_template_name': 'userprofile/password_reset_email.txt',
                'html_email_template_name': 'userprofile/password_reset_email.html',
                'subject_template_name': 'userprofile/password_reset_subject.txt'
                }),
    url(r'^password-reset-done/$', auth_views.password_reset_done, name='password_reset_done',
        kwargs={'template_name': 'userprofile/password_reset_done.html', }),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm',
        kwargs={'template_name': 'userprofile/password_reset_confirm.html'}),
    url(r'^password-reset-completed/$', auth_views.password_reset_complete, name='password_reset_complete',
        kwargs={'template_name': 'userprofile/password_reset_complete.html'}),
]
