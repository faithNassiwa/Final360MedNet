from django.conf.urls import url
from website import views as website_views

urlpatterns = [
    url(r'^about-360MedNet/$', website_views.about_us, name='about_us'),
    url(r'^privacy-policy/$', website_views.privacy_policy, name='privacy_policy'),
    url(r'^terms-of-use/$', website_views.terms_of_use, name='terms_of_use'),
    url(r'^help/$', website_views.website_help, name='help'),
]
