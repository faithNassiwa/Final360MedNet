from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse
from .forms import DoctorForm, UserForm, VerifyForm, ProfileForm, SocialSiteForm, QualificationForm
from .models import Medic, Doctor, Qualification
from django.views.generic.edit import UpdateView, CreateView
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from invitation.models import Invitation


class EmailAuthenticationForm(AuthenticationForm):
    def clean_username(self):
        username = self.data['username']
        if '@' in username:
            try:
                username = User.objects.get(email=username).username
            except ObjectDoesNotExist:
                raise ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
        return username


def verify(request):
    form = VerifyForm(data=request.POST)
    verified = False
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        surname = form.cleaned_data['surname']
        other_name = form.cleaned_data['other_name']
        if Medic.objects.filter(email__iexact=email, surname__iexact=surname, other_name__iexact=other_name,
                                status=False).exists():
            qs = Medic.objects.get(email=email)
            return HttpResponseRedirect('/accounts/verified_registration/{}'.format(qs))
        elif Medic.objects.filter(email__iexact=email, surname__iexact=surname,
                                  other_name__iexact=other_name,
                                  status=True).exists():
            return HttpResponseRedirect("/accounts/login")
        else:
            qs = {'other_name': other_name}
            return HttpResponseRedirect('/accounts/unverified_registration/', {'qs': qs})

    return render(request, 'userprofile/verify.html', {'form': form, 'verified': verified})


def register(request, reg_number):
    qs = Medic.objects.filter(reg_number=reg_number).all()
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        doctor_form = DoctorForm(data=request.POST)
        if user_form.is_valid() and doctor_form.is_valid():
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']
            username = user_form.cleaned_data['username']
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            doctor = doctor_form.save(commit=False)
            doctor.verification_status = True
            doctor.user = user
            doctor.save()
            registered = True
            qs.update(status=True)
            current_site = get_current_site(request)
            subject = 'Welcome to 360MedNet.'
            message = render_to_string('userprofile/thank_you_signup_email.html', {
                'user': user,
                'doctor': doctor,
                'domain': current_site.domain,
                'password': password

            })
            to_email = email
            email = EmailMultiAlternatives(subject, message, to=[to_email])
            email.attach_alternative(message, "text/html")
            email.send()

        else:
            print(user_form.errors, doctor_form.errors)

    else:
        user_form = UserForm()
        doctor_form = DoctorForm()

    return render(request, 'userprofile/register.html', locals())


def unverified_register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        doctor_form = DoctorForm(data=request.POST)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()
            registered = True
            current_site = get_current_site(request)
            subject = 'Welcome to 360MedNet.'
            message = render_to_string('userprofile/thank_you_signup_email.html', {
                'user': user,
                'doctor': doctor,
                'domain': current_site.domain,
                'password': user.password

            })
            to_email = user.email
            email = EmailMultiAlternatives(subject, message, to=[to_email])
            email.attach_alternative(message, "text/html")
            email.send()

        else:
            print(user_form.errors, doctor_form.errors)

    else:
        user_form = UserForm()
        doctor_form = DoctorForm()

    return render(request, 'userprofile/unverified_register.html', locals())


@login_required(login_url='/login/')
def get_profile(request, username):
    user = User.objects.get(username=username)
    doctor = Doctor.objects.get(user=user)
    read_profile = Doctor.objects.get(user=user)
    read_qualification = Qualification.objects.filter(doctor=doctor).all()

    return render(request, 'userprofile/read_profile.html', {'read_profile': read_profile, 'user': user,
                                                             'read_qualification': read_qualification})


class DoctorDetail(DetailView):
    model = Doctor

    def get_context_data(self, **kwargs):
        context = super(DoctorDetail, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class UpdateProfile(UpdateView):
    model = Doctor
    form_class = ProfileForm

    template_name = 'userprofile/doctor_profile_update.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.doctor = Doctor.objects.get(user=self.request.user)
        return super(UpdateProfile, self).form_valid(form)


class QualificationCreate(CreateView):
    model = Qualification
    form_class = QualificationForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.doctor = Doctor.objects.get(user=self.request.user)
        instance.save()
        return super(QualificationCreate, self).form_valid(form)


class QualificationDetail(DetailView):
    model = Qualification

    def get_context_data(self, **kwargs):
        context = super(QualificationDetail, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class UpdateQualification(UpdateView):
    model = Qualification
    fields = ['qualification', 'university']

    template_name = 'userprofile/doctor_profile_update.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.doctor = Doctor.objects.get(user=self.request.user)
        return super(UpdateQualification, self).form_valid(form)


def home(request):
    return render(request, 'userprofile/home.html')


def signup(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            invitation = Invitation(
                name=form.cleaned_data['other_name'],
                organization=form.cleaned_data['organization'],
                email=form.cleaned_data['alternative_email'],
                code=User.objects.make_random_password(6)
            )

            invitation.save()
            invitation.send_invite()
            messages.success(request, message='An invitation has been sent to  %s, please check your email to '
                                              'access next steps.' % invitation.email
                             )
            Medic.objects.filter(other_name__iexact=form.cleaned_data['other_name'],
                                 surname__iexact=form.cleaned_data['surname']). \
                update(verification_status=True, invitation_status=True)

    else:
        form = VerifyForm()
    return render(request, 'userprofile/signup.html', {'form': form})


def signup_activate(request):
    return render(request, 'userprofile/signup_activate.html')


class RegisterUpdateView(UpdateView):
    model = Doctor
    fields = ['first_name', 'last_name', 'profession', 'country']

    template_name = 'userprofile/register_update.html'
    success_url = 'login'
