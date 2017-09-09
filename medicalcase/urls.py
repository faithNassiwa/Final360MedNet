from django.conf.urls import url
from medicalcase import views as medicalcase_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^post/medical-case/$', login_required(medicalcase_views.MedicalCaseCreate.as_view()), name='medical-case'),
    url(r'^medical-cases/$', login_required(medicalcase_views.MedicalCaseList.as_view(paginate_by=5)),
        name='medical_cases'),
    url(r'^medical-case/(?P<pk>[0-9]+)/detail/$', login_required(medicalcase_views.MedicalCaseDetail.as_view()),
        name='medical-case-detail'),
    url(r'medical-case/comment/(?P<pk>[0-9]+)/$', medicalcase_views.medical_case_comment_add_view,
        name='medical-case-comment'),
    url(r'^send/medical-cases/$', login_required(medicalcase_views.send_top_five_medical_cases_weekly),
        name='send-medical-case'),

    url(r'^view/medical-cases/email/$', login_required(medicalcase_views.view_medical_case_email),
        name='view-medical-case-email'),

]
