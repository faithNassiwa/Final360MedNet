from django import forms
from django.contrib.auth.models import User
from material.base import Layout, Row, Fieldset
from userprofile.models import Doctor, SocialSite, Qualification, Medic
from invitation.models import Invitation
from django_countries.widgets import CountrySelectWidget


def email_already_registered_or_invited(value):
    if User.objects.filter(email=value).exists():
        raise forms.ValidationError("Email provided is already registered with 360MedNet.")
    elif Invitation.objects.filter(email=value, accepted=False).exists():
        raise forms.ValidationError("Email provided was already invited and has not yet accepted the invitation.")
    elif Invitation.objects.filter(email=value, accepted=True).exists():
        raise forms.ValidationError("Email provided was already invited and accepted the invitation")
    else:
        pass


class VerifyForm(forms.Form):
    other_name = forms.CharField(max_length=200, label="First Name(s)")
    surname = forms.CharField(max_length=200)
    alternative_email = forms.EmailField(required=False, label="Your primary email address")
    organization = forms.CharField(required=False, label="Organization, Hostpital or Company")

    layout = Layout(
        Row('other_name', 'surname'),
        'alternative_email',
        'organization'

    )

    def clean(self):
        cleaned_data = super(VerifyForm, self).clean()
        other_name = cleaned_data.get("other_name")
        surname = cleaned_data.get("surname")

        try:
            Medic.objects.get(surname__iexact=surname, other_name__iexact=other_name)
            pass

        except Medic.DoesNotExist:
            raise forms.ValidationError("%s %s does not exist in our database. Please provide your registered name as "
                                        "they appear on your medical license" % (other_name, surname))

        # except Medic.objects.get(surname__iexact=surname, other_name__iexact=other_name, invitation_status=True,
        #                          verification_status=True):
        #     raise forms.ValidationError("%s %s was already invited to join 360MedNet. Please check your email for "
        #                                 "the invitation." % (other_name, surname))
        return self.cleaned_data


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(label="Email Address")

    layout = Layout(Row('email', 'password')

                    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)


class DoctorForm(forms.ModelForm):
    country = forms.CharField(label="Country of Practice")
    layout = Layout(Fieldset('Personal details',
                             Row('first_name', 'last_name'),
                             'profession', 'specialization', 'country'
                             ))

    class Meta:
        model = Doctor
        fields = ('first_name', 'last_name', 'profession', 'specialization', 'country')
        widgets = {'country': CountrySelectWidget()}


class SocialSiteForm(forms.ModelForm):
    class Meta:
        model = SocialSite
        fields = ('doctor', 'social_site', 'username')


class ProfileForm(forms.ModelForm):
    layout = Layout(Fieldset('Personal details',
                             Row('first_name', 'middle_name', 'last_name'),
                             Row('gender', 'date_of_birth'), 'about_me', 'mobile_number',
                             ),
                    Fieldset('Professional details',
                             Row('profession', 'specialization'),
                             Row('year_of_first_medical_certification', 'hospital'),
                             Row('country', 'city'), 'work_number',
                             ),
                    'avatar'
                    )

    class Meta:
        model = Doctor
        fields = ('first_name', 'middle_name', 'last_name', 'gender', 'date_of_birth', 'profession',
                  'specialization', 'country', 'city', 'year_of_first_medical_certification', 'mobile_number',
                  'about_me', 'hospital', 'work_number', 'avatar')


class QualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ('field_of_study', 'qualification', 'university')

