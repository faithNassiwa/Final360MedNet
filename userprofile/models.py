import os
from django.db import models
from django.contrib.auth.models import User
import csv
from django.core.files.storage import default_storage
import urllib.request
import codecs
from PIL import Image
from django.urls import reverse
import io
import requests
from contextlib import closing
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from invitation.models import Invitation
from django_countries.fields import CountryField


COUNTRIES = (
    ('UG', 'Uganda'),
    ('Afghanistan', 'Afghanistan'),
    ('Aland Islands', 'Aland Islands'),
    ('Albania', 'Albania'),
    ('Algeria', 'Algeria'),
    ('American Samoa', 'American Samoa'),
    ('Andorra', 'Andorra'),
    ('Angola', 'Angola'),
    ('Anguilla', 'Anguilla'),
    ('Antarctica', 'Antarctica'),
    ('Antigua and Barbuda', 'Antigua and Barbuda'),
    ('Argentina', 'Argentina'),
    ('Armenia', 'Armenia'),
    ('Aruba', 'Aruba'),
    ('Australia', 'Australia'),
    ('Austria', 'Austria'),
    ('Azerbaijan', 'Azerbaijan'),
    ('Bahamas', 'Bahamas'),
    ('Bahrain', 'Bahrain'),
    ('Bangladesh', 'Bangladesh'),
    ('Barbados', 'Barbados'),
    ('Belarus', 'Belarus'),
    ('Belgium', 'Belgium'),
    ('Belize', 'Belize'),
    ('Benin', 'Benin'),
    ('Bermuda', 'Bermuda'),
    ('Bhutan', 'Bhutan'),
    ('Bolivia', 'Bolivia'),
    ('Bosnia and Herzegovina', 'Bosnia and Herzegovina'),
    ('Botswana', 'Botswana'),
    ('Bouvet Island', 'Bouvet Island'),
    ('Brazil', 'Brazil'),
    ('British Indian Ocean Territory', 'British Indian Ocean Territory'),
    ('Brunei Darussalam', 'Brunei Darussalam'),
    ('Bulgaria', 'Bulgaria'),
    ('Burkina Faso', 'Burkina Faso'),
    ('Burundi', 'Burundi'),
    ('Cambodia', 'Cambodia'),
    ('Cameroon', 'Cameroon'),
    ('Canada', 'Canada'),
    ('Cape Verde', 'Cape Verde'),
    ('Cayman Islands', 'Cayman Islands'),
    ('Central African Republic', 'Central African Republic'),
    ('Chad', 'Chad'),
    ('Chile', 'Chile'),
    ('China', 'China'),
    ('Christmas Island', 'Christmas Island'),
    ('Cocos (Keeling) Islands', 'Cocos (Keeling) Islands'),
    ('Colombia', 'Colombia'),
    ('Comoros', 'Comoros'),
    ('Congo', 'Congo'),
    ('Congo, The Democratic Republic of the', 'Congo, The Democratic Republic of the'),
    ('Cook Islands', 'Cook Islands'),
    ('Costa Rica', 'Costa Rica'),
    ('Cote d\'Ivoire', 'Cote d\'Ivoire'),
    ('Croatia', 'Croatia'),
    ('Cuba', 'Cuba'),
    ('Cyprus', 'Cyprus'),
    ('Czech Republic', 'Czech Republic'),
    ('Denmark', 'Denmark'),
    ('Djibouti', 'Djibouti'),
    ('Dominica', 'Dominica'),
    ('Dominican Republic', 'Dominican Republic'),
    ('Ecuador', 'Ecuador'),
    ('Egypt', 'Egypt'),
    ('El Salvador', 'El Salvador'),
    ('Equatorial Guinea', 'Equatorial Guinea'),
    ('Eritrea', 'Eritrea'),
    ('Estonia', 'Estonia'),
    ('Ethiopia', 'Ethiopia'),
    ('Falkland Islands (Malvinas)', 'Falkland Islands (Malvinas)'),
    ('Faroe Islands', 'Faroe Islands'),
    ('Fiji', 'Fiji'),
    ('Finland', 'Finland'),
    ('France', 'France'),
    ('French Guiana', 'French Guiana'),
    ('French Polynesia', 'French Polynesia'),
    ('French Southern Territories', 'French Southern Territories'),
    ('Gabon', 'Gabon'),
    ('Gambia', 'Gambia'),
    ('Georgia', 'Georgia'),
    ('Germany', 'Germany'),
    ('Ghana', 'Ghana'),
    ('Gibraltar', 'Gibraltar'),
    ('Greece', 'Greece'),
    ('Greenland', 'Greenland'),
    ('Grenada', 'Grenada'),
    ('Guadeloupe', 'Guadeloupe'),
    ('Guam', 'Guam'),
    ('Guatemala', 'Guatemala'),
    ('Guinea', 'Guinea'),
    ('Guinea-Bissau', 'Guinea-Bissau'),
    ('Guyana', 'Guyana'),
    ('Haiti', 'Haiti'),
    ('Heard Island and McDonald Islands', 'Heard Island and McDonald Islands'),
    ('Holy See (Vatican City State)', 'Holy See (Vatican City State)'),
    ('Honduras', 'Honduras'),
    ('Hong Kong', 'Hong Kong'),
    ('Hungary', 'Hungary'),
    ('Iceland', 'Iceland'),
    ('India', 'India'),
    ('Indonesia', 'Indonesia'),
    ('Iran, Islamic Republic of', 'Iran, Islamic Republic of'),
    ('Iraq', 'Iraq'),
    ('Ireland', 'Ireland'),
    ('Isle of Man', 'Isle of Man'),
    ('Israel', 'Israel'),
    ('Italy', 'Italy'),
    ('Jamaica', 'Jamaica'),
    ('Japan', 'Japan'),
    ('Jersey', 'Jersey'),
    ('Jordan', 'Jordan'),
    ('Kazakhstan', 'Kazakhstan'),
    ('Kenya', 'Kenya'),
    ('Kiribati', 'Kiribati'),
    ('Korea, Democratic People\'s Republic of', 'Korea, Democratic People\'s Republic of'),
    ('Korea, Republic of', 'Korea, Republic of'),
    ('Kuwait', 'Kuwait'),
    ('Kyrgyzstan', 'Kyrgyzstan'),
    ('Lao People\'s Democratic Republic', 'Lao People\'s Democratic Republic'),
    ('Latvia', 'Latvia'),
    ('Lebanon', 'Lebanon'),
    ('Lesotho', 'Lesotho'),
    ('Liberia', 'Liberia'),
    ('Libyan Arab Jamahiriya', 'Libyan Arab Jamahiriya'),
    ('Liechtenstein', 'Liechtenstein'),
    ('Lithuania', 'Lithuania'),
    ('Luxembourg', 'Luxembourg'),
    ('Macao', 'Macao'),
    ('Macedonia, The Former Yugoslav Republic of', 'Macedonia, The Former Yugoslav Republic of'),
    ('Madagascar', 'Madagascar'),
    ('Malawi', 'Malawi'),
    ('Malaysia', 'Malaysia'),
    ('Maldives', 'Maldives'),
    ('Mali', 'Mali'),
    ('Malta', 'Malta'),
    ('Marshall Islands', 'Marshall Islands'),
    ('Martinique', 'Martinique'),
    ('Mauritania', 'Mauritania'),
    ('Mauritius', 'Mauritius'),
    ('Mayotte', 'Mayotte'),
    ('Mexico', 'Mexico'),
    ('Micronesia, Federated States of', 'Micronesia, Federated States of'),
    ('Moldova', 'Moldova'),
    ('Monaco', 'Monaco'),
    ('MMongoliaN', 'Mongolia'),
    ('Montenegro', 'Montenegro'),
    ('Montserrat', 'Montserrat'),
    ('Morocco', 'Morocco'),
    ('Mozambique', 'Mozambique'),
    ('Myanmar', 'Myanmar'),
    ('Namibia', 'Namibia'),
    ('Nauru', 'Nauru'),
    ('Nepal', 'Nepal'),
    ('Netherlands', 'Netherlands'),
    ('Netherlands Antilles', 'Netherlands Antilles'),
    ('New Caledonia', 'New Caledonia'),
    ('New Zealand', 'New Zealand'),
    ('Nicaragua', 'Nicaragua'),
    ('Niger', 'Niger'),
    ('Nigeria', 'Nigeria'),
    ('Niue', 'Niue'),
    ('Norfolk Island', 'Norfolk Island'),
    ('Northern Mariana Islands', 'Northern Mariana Islands'),
    ('Norway', 'Norway'),
    ('Oman', 'Oman'),
    ('Pakistan', 'Pakistan'),
    ('Palau', 'Palau'),
    ('Palestinian Territory, Occupied', 'Palestinian Territory, Occupied'),
    ('Panama', 'Panama'),
    ('Papua New Guinea', 'Papua New Guinea'),
    ('Paraguay', 'Paraguay'),
    ('Peru', 'Peru'),
    ('Philippines', 'Philippines'),
    ('Pitcairn', 'Pitcairn'),
    ('Poland', 'Poland'),
    ('Portugal', 'Portugal'),
    ('Puerto Rico', 'Puerto Rico'),
    ('Qatar', 'Qatar'),
    ('Reunion', 'Reunion'),
    ('Romania', 'Romania'),
    ('Russian Federation', 'Russian Federation'),
    ('Rwanda', 'Rwanda'),
    ('Saint Barthelemy', 'Saint Barthelemy'),
    ('Saint Helena', 'Saint Helena'),
    ('Saint Kitts and Nevis', 'Saint Kitts and Nevis'),
    ('Saint Lucia', 'Saint Lucia'),
    ('Saint Martin', 'Saint Martin'),
    ('Saint Pierre and Miquelon', 'Saint Pierre and Miquelon'),
    ('Saint Vincent and the Grenadines', 'Saint Vincent and the Grenadines'),
    ('Samoa', 'Samoa'),
    ('San Marino', 'San Marino'),
    ('Sao Tome and Principe', 'Sao Tome and Principe'),
    ('Saudi Arabia', 'Saudi Arabia'),
    ('Senegal', "Senegal"),
    ('Serbia', 'Serbia'),
    ('Seychelles', 'Seychelles'),
    ('Sierra Leone', 'Sierra Leone'),
    ('Singapore', 'Singapore'),
    ('Slovakia', 'Slovakia'),
    ('Slovenia', 'Slovenia'),
    ('Solomon Islands', 'Solomon Islands'),
    ('Somalia', 'Somalia'),
    ('South Africa', 'South Africa'),
    ('South Georgia and the South Sandwich Islands', 'South Georgia and the South Sandwich Islands'),
    ('Spain', 'Spain'),
    ('Sri Lanka', 'Sri Lanka'),
    ('Sudan', 'Sudan'),
    ('Suriname', 'Suriname'),
    ('Svalbard and Jan Mayen', 'Svalbard and Jan Mayen'),
    ('Swaziland', 'Swaziland'),
    ('Sweden', 'Sweden'),
    ('Switzerland', 'Switzerland'),
    ('Syrian Arab Republic', 'Syrian Arab Republic'),
    ('Taiwan, Province of China', 'Taiwan, Province of China'),
    ('Tajikistan', 'Tajikistan'),
    ('Tanzania, United Republic of', 'Tanzania, United Republic of'),
    ('Thailand', 'Thailand'),
    ('Timor-Leste', 'Timor-Leste'),
    ('Togo', 'Togo'),
    ('Tokelau', 'Tokelau'),
    ('Tonga', 'Tonga'),
    ('Trinidad and Tobago', 'Trinidad and Tobago'),
    ('Tunisia', 'Tunisia'),
    ('Turkey', 'Turkey'),
    ('Turkmenistan', 'Turkmenistan'),
    ('Turks and Caicos Islands', 'Turks and Caicos Islands'),
    ('Tuvalu', 'Tuvalu'),
    ('Uganda', 'Uganda'),
    ('Ukraine', 'Ukraine'),
    ('United Arab Emirates', 'United Arab Emirates'),
    ('United Kingdom', 'United Kingdom'),
    ('United States', 'United States'),
    ('United States Minor Outlying Islands', 'United States Minor Outlying Islands'),
    ('Uruguay', 'Uruguay'),
    ('Uzbekistan', 'Uzbekistan'),
    ('Vanuatu', 'Vanuatu'),
    ('Venezuela', 'Venezuela'),
    ('Viet Nam', 'Viet Nam'),
    ('Virgin Islands, British', 'Virgin Islands, British'),
    ('Virgin Islands, U.S.', 'Virgin Islands, U.S.'),
    ('Wallis and Futuna', 'Wallis and Futuna'),
    ('Western Sahara', 'Western Sahara'),
    ('Yemen', 'Yemen'),
    ('Zambia', 'Zambia'),
    ('Zimbabwe', 'Zimbabwe'),
)


class Profession(models.Model):
    profession = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name_plural = 'Professions'

    def __str__(self):
        return str(self.profession)


class Specialization(models.Model):
    specialization = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name_plural = 'Specializations'

    def __str__(self):
        return str(self.specialization)


class Doctor(models.Model):
    user = models.OneToOneField(User)
    GENDER = (('Female', 'Female'), ('Male', 'Male'))
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    gender = models.CharField(max_length=6, choices=GENDER)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    profession = models.ForeignKey(Profession)
    specialization = models.ForeignKey(Specialization, blank=True, null=True)
    year_of_first_medical_certification = models.CharField(max_length=4)
    mobile_number = models.CharField(max_length=30, blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True, choices=COUNTRIES)
    # country = CountryField(blank_label='Select country of practice')
    city = models.CharField(max_length=30, blank=True, null=True)
    hospital = models.CharField(max_length=30, blank=True, null=True)
    work_number = models.CharField(max_length=30, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars", default='avatars/default.jpeg', height_field=None,
                               width_field=None, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    invitation_code = models.CharField(max_length=17, blank=True, null=True)
    invitation_code_object = models.ForeignKey(Invitation, blank=True, null=True)
    verification_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return ' %s %s' % (self.first_name, self.last_name)

    @classmethod
    def view_profile(cls):
        return cls.objects.all()

    def get_absolute_url(self):
        return reverse('doctor-detail', kwargs={'pk': self.pk})

    def send_login_credentials(self):
        subject = 'Complete Registration on 360MedNet'
        link = 'http://%s/join/%s/' % (
            settings.SITE_HOST,
            self.code
        )
        template = get_template('invitation/emails/invitation_email.html')
        context = Context({
            'name': self.name,
            'organization': self.organization,
            'link': link,
        })
        message = template.render(context)
        send_mail(
            subject, message,
            settings.EMAIL_HOST_USER, [self.email]
        )


class Qualification(models.Model):
    qualification = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    doctor = models.ForeignKey(Doctor)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return str(self.qualification)

    def get_absolute_url(self):
        return reverse('qualification-detail', kwargs={'pk': self.pk})


class SocialSite(models.Model):
    SOCIAL_SITE = (('LinkedIn', 'LinkedIn'), ('Facebook', 'Facebook'), ('Twitter', 'Twitter'), ('Youtube', 'Youtube'))

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    social_site = models.CharField(max_length=50, choices=SOCIAL_SITE)
    username = models.CharField(max_length=100)

    def __str__(self):
        return '%s', self.doctor_id


class Record(models.Model):
    FILE_CATEGORY = (('Medical Records DB File', 'Medical Records DB file'),
                     ('Gathered inhouse emails', 'Gathered inhouse emails'))
    file = models.FileField(upload_to="records")
    file_category = models.CharField(max_length=20, choices=FILE_CATEGORY)
    synced = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_record_file(cls):
        if cls.objects.filter(synced=False, file_category='Medical Records DB File').exists():
            csv_file = cls.objects.filter(synced=False, file_category='Medical Records DB File').first().file
            Medic.create_medic(csv_file=csv_file)
        elif cls.objects.filter(synced=False, file_category='Gathered inhouse emails').exists():
            csv_file = cls.objects.filter(synced=False, file_category='Medical Records DB File').first().file
            MedicEmail.create_medic(csv_file=csv_file)
        else:
            print("All files synced")

    def __str__(self):
        return str(self.file)


class Medic(models.Model):
    reg_number = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    other_name = models.CharField(max_length=100)
    email = models.EmailField()
    sex = models.CharField(max_length=6)
    employer = models.CharField(max_length=100)
    postal_address = models.CharField(max_length=100)
    first_registration = models.CharField(max_length=100)
    date_of_first_registration = models.CharField(max_length=100)
    additional_qualifications = models.TextField()
    speciality = models.CharField(max_length=100)
    receipt_number = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    invitation_status = models.BooleanField(default=False)
    verification_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    @classmethod
    def create_medic(cls, csv_file):
        medical_practitioner = 0

        # url = "https://360mednet.s3.amazonaws.com/%s" % csv_file
        # ftpstream = urllib.request.urlopen(url)
        # csvfile = csv.reader(ftpstream.read().decode('ISO-8859-1'))
        # csvfile = csv.reader(url)
        # csvfile = csv.reader(io.TextIOWrapper(ftpstream))
        with default_storage.open(os.path.join(str(csv_file)), 'rt') as f:
            f = default_storage.open(os.path.join(str(csv_file)), 'r')
            csvfile = csv.reader(f)

        for row in csvfile:
            reg_number = row[0]
            if not Medic.medic_exists(reg_number):
                Medic.objects.create(reg_number=row[0], surname=row[1], other_name=row[2],
                                     sex=row[3], employer=row[4], postal_address=row[5],
                                     first_registration=row[6],
                                     date_of_first_registration=row[7],
                                     additional_qualifications=row[8], speciality=row[9],
                                     receipt_number=row[10], serial_number=row[11]
                                     )
                medical_practitioner = + 1
            else:
                Medic.objects.filter(reg_number=row[0]).update(surname=row[1], other_name=row[2],
                                                               sex=row[3], employer=row[4], postal_address=row[5],
                                                               first_registration=row[6],
                                                               date_of_first_registration=row[7],
                                                               additional_qualifications=row[8], speciality=row[9],
                                                               receipt_number=row[10], serial_number=row[11]
                                                               )
                medical_practitioner = + 1

            Record.objects.filter(file=csv_file).update(synced=True)
        return medical_practitioner

    @classmethod
    def medic_exists(cls, reg_number):
        return cls.objects.filter(reg_number=reg_number).exists()

    def __str__(self):
        return self.reg_number


class MedicEmail(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    invitation_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    @classmethod
    def create_medic(cls, csv_file):
        medical_practitioner = 0

        # url = "https://360mednet.s3.amazonaws.com/%s" % csv_file
        # ftpstream = urllib.request.urlopen(url)
        # csvfile = csv.reader(ftpstream.read().decode('ISO-8859-1'))
        # csvfile = csv.reader(url)
        # csvfile = csv.reader(io.TextIOWrapper(ftpstream))
        with default_storage.open(os.path.join(str(csv_file)), 'rt') as f:
            f = default_storage.open(os.path.join(str(csv_file)), 'r')
            csvfile = csv.reader(f)

        for row in csvfile:
            email = row[2]
            if not Medic.medic_exists(email):
                Medic.objects.create(name=row[0], profession=row[1], email=row[2])
                medical_practitioner = + 1
            else:
                Medic.objects.filter(email=row[2]).update(name=row[0], profession=row[1])
                medical_practitioner = + 1

            Record.objects.filter(file=csv_file).update(synced=True)
        return medical_practitioner

    @classmethod
    def medic_exists(cls, email):
        return cls.objects.filter(email=email).exists()

    def __str__(self):
        return self.name

