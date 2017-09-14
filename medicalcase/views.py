from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import MedicalCase, MedicalCaseCategory, Comment
from userprofile.models import Doctor
from .forms import MedicalCaseForm
from django.views.generic.edit import DeleteView, ModelFormMixin
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, MedicalCaseSearchForm
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from post.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class MedicalCaseCreate(CreateView):
    model = MedicalCase
    form_class = MedicalCaseForm

    success_url = '/medical-cases/'
    template_name = 'medicalcase/medicalcase_form.html'

    def form_valid(self, form):
        form.instance.doctor = Doctor.objects.get(user=self.request.user)
        form.instance.save()
        return super(MedicalCaseCreate, self).form_valid(form)


class MedicalCaseList(ListView):
    model = MedicalCase
    form_class = MedicalCaseSearchForm
    template_name = 'medicalcase/medicalcase_list.html'
    context_object_name = 'medical_cases'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(MedicalCaseList, self).get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return MedicalCase.objects.filter(medical_case_category__in=
                                              form.cleaned_data['medical_case_category'])
        return MedicalCase.objects.all()


class MedicalCaseDetail(ModelFormMixin, DetailView):
    model = MedicalCase
    form_class = CommentForm

    def get_success_url(self):
        return reverse('medical-case-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(MedicalCaseDetail, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def comments(self):
        return Comment.objects.filter(medical_case=MedicalCase.objects.get(pk=self.object.pk)).all().order_by(
            '-created_at')


@login_required
def medical_case_comment_add_view(request, pk):
    form = CommentForm(request.POST or None)

    if form.is_valid() and pk:
        form.instance.doctor = Doctor.objects.get(user=request.user)
        form.instance.medical_case = MedicalCase.objects.get(pk=pk)
        form.save()
        return HttpResponseRedirect(reverse('medical_case-detail', kwargs={'pk': pk}))
    return HttpResponseRedirect(reverse('medical_case-detail', kwargs={'pk': pk}))


@login_required
def send_top_five_medical_cases_weekly(request):
    weekly_five_medical_cases = MedicalCase.weekly_top_five_medical_case()
    subject_medical_case = MedicalCase.objects.last()
    weekly_top_five_discussions = Post.weekly_top_five_discussions()
    registered_doctors = Doctor.objects.all()
    # registered_doctors_mailing_list = []
    for registered_doctor in registered_doctors:
        # registered_doctors_mailing_list.append(registered_doctor.user.email) ## might need to accesss name of the docs

        current_site = get_current_site(request)
        subject = subject_medical_case.title
        message = render_to_string('medicalcase/medicalcase_email_update.html', {
            'weekly_five_medical_cases': weekly_five_medical_cases,
            'weekly_top_five_discussions': weekly_top_five_discussions,
            'doctor': registered_doctor,
            'domain': current_site.domain,

        })
        to_email1 = registered_doctor.user.email
        email = EmailMessage(subject, message, to=[to_email1])
        email.content_subtype = "html"
        email.send()

    return HttpResponse("Successfully sent")


@login_required
def view_medical_case_email(request):
    return render(request, 'medicalcase/medicalcase_email_update.html')
