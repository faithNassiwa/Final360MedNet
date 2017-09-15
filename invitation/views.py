from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from userprofile.models import Doctor
from .forms import MedicInvitationForm, FriendInvitationForm, RegistrationForm1, RegistrationForm2, RegistrationForm3, \
    SuggestedInviteeForm
from .models import Invitation, FriendInvitation
from django.contrib.auth.models import User
from userprofile.forms import DoctorForm, UserForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from userprofile.models import MedicEmail
from django.template import Context
from django.conf import settings

home = settings.SITE_HOST


@staff_member_required
def invite_user(request):
    if request.method == 'POST':
        form = MedicInvitationForm(request.POST)
        if form.is_valid():

            invitation = Invitation(
                name=form.cleaned_data['name'],
                organization=form.cleaned_data['organization'],
                email=form.cleaned_data['email'],
                code=User.objects.make_random_password(6)
            )
            if invitation.email:
                invitation.save()
                invitation.send_invite()
                messages.success(request,
                                 message='Invitation successfully sent to %s.' %
                                         invitation.email
                                 )
    else:
        form = MedicInvitationForm()

    return render(request, 'invitation/user_invite.html', {'form': form})


@staff_member_required
def bulk_invite(request):
    medics = MedicEmail.objects.filter(invitation_status=False).all()
    invited_medics = 0
    if medics.count() > 0:
        for medic in medics:
            invitation = Invitation(
                name=medic.name,
                email=medic.email,
                code=User.objects.make_random_password(6)
            )
            if invitation.email and not User.objects.filter(email=invitation.email).exists():
                invitation.save()
                invitation.send_invite()
                MedicEmail.objects.filter(email=invitation.email).update(invitation_status=True)
                invited_medics += 1

    return HttpResponse('Successfully invited %s medics via email' % invited_medics)


def invite_friend(request):
    if request.method == 'POST':
        form = FriendInvitationForm(request.POST)
        if form.is_valid():

            friend_invitation = FriendInvitation(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                code=User.objects.make_random_password(8),
                sender=request.user
            )
            if friend_invitation.email and not User.objects.filter(email=friend_invitation.email).exists():
                friend_invitation.save()
                friend_invitation.send_invite()
                messages.success(request, 'Invitation sent')
            else:
                messages.error(request, 'Invitation not sent, email already registered with 360MedNet')
    else:
        form = FriendInvitationForm()

    return render(request, 'invitation/friend_invite.html', {'form': form})


def join(request, code):
    invitation = get_object_or_404(Invitation, code__exact=code)
    request.session['invitation'] = invitation.id
    return HttpResponseRedirect('/register_medic/')


def join_friend_invite(request, code):
    friend_invitation = get_object_or_404(FriendInvitation, code__exact=code)
    request.session['friend_invitation'] = friend_invitation.id
    return HttpResponseRedirect('/register_medic/')


def register_invited_user(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        doctor_form = DoctorForm(data=request.POST)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            doctor = doctor_form.save(commit=False)
            doctor.verification_status = True
            doctor.user = user
            doctor.save()
            if FriendInvitation.objects.filter(email=user.email).exists():
                FriendInvitation.objects.filter(email=user.email).update(accepted=True)
            else:
                Invitation.objects.filter(email=user.email).update(accepted=True)

            registered = True

        else:
            print(user_form.errors, doctor_form.errors)

    else:
        user_form = UserForm()
        doctor_form = DoctorForm()

    return render(request, 'userprofile/register.html', locals())


def registration_one(request):
    initial = {'first_name': request.session.get('first_name', None),
               'last_name': request.session.get('last_name', None),
               'invitation_code': request.session.get('invitation_code', None)}
    form = RegistrationForm1(request.POST or None, initial=initial)
    if request.method == 'POST':
        if form.is_valid():
            request.session['first_name'] = form.cleaned_data['first_name']
            request.session['last_name'] = form.cleaned_data['last_name']
            request.session['invitation_code'] = form.cleaned_data['invitation_code']
            context = Context({
                'first_name': request.session['first_name'],
                'domain': home})

            Invitation.send_signup_email(context, request.session['invitation_code'])
            return HttpResponseRedirect(reverse('reg_2'))
    return render(request, 'invitation/registration_one.html', {'form': form})


def registration_two(request):
    doctor_form = RegistrationForm3(request.POST or None)
    user_form = RegistrationForm2(request.POST or None)
    first_name = request.session['first_name']
    last_name = request.session['last_name']
    if request.method == 'POST':
        if doctor_form.is_valid() and user_form.is_valid():
            user = user_form.save()
            user.username = first_name + "-" + last_name + "-" + User.objects.make_random_password(8)
            user.first_name = request.session['first_name']
            user.last_name = request.session['last_name']
            user.set_password(user.password)
            user.save()
            doctor = doctor_form.save(commit=False)
            doctor = Doctor.objects.create(first_name=request.session['first_name'],
                                           last_name=request.session['last_name'],
                                           invitation_code=request.session['invitation_code'],
                                           invitation_code_object=Invitation.objects.
                                           get(code=request.session['invitation_code']),
                                           profession=doctor.profession,
                                           country=doctor.country, user=user,
                                           verification_status=True)

            context = Context({
                'user': user,
                'doctor': doctor,
                'domain': home,

            })
            Invitation.send_thank_you_for_signing_up_email(context, user)

            return HttpResponseRedirect(reverse('finished'))
    return render(request, 'invitation/registration_two.html', {'doctor_form': doctor_form, 'user_form': user_form,
                                                                'first_name': first_name, 'last_name': last_name})


def done(request):
    return render(request, 'invitation/done.html')


def send_suggested_invitee(request):
    form = SuggestedInviteeForm()
    if request.method == 'POST':
        form = SuggestedInviteeForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.doctor = request.user
            instance.save()
            messages.success(request, message="%s's invite request has been received and will be invited once "
                                              "verified." % instance.name)

    return render(request, 'invitation/suggest_invitee.html', locals())
