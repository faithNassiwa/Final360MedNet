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


# COUNTRIES = (
#     ('GB', 'United Kingdom'),
#     ('AF', 'Afghanistan'),
#     ('AX', 'Aland Islands'),
#     ('AL', 'Albania'),
#     ('DZ', 'Algeria'),
#     ('AS', 'American Samoa'),
#     ('AD', 'Andorra'),
#     ('AO', 'Angola'),
#     ('AI', 'Anguilla'),
#     ('AQ', 'Antarctica'),
#     ('AG', 'Antigua and Barbuda'),
#     ('AR', 'Argentina'),
#     ('AM', 'Armenia'),
#     ('AW', 'Aruba'),
#     ('AU', 'Australia'),
#     ('AT', 'Austria'),
#     ('AZ', 'Azerbaijan'),
#     ('BS', 'Bahamas'),
#     ('BH', 'Bahrain'),
#     ('BD', 'Bangladesh'),
#     ('BB', 'Barbados'),
#     ('BY', 'Belarus'),
#     ('BE', 'Belgium'),
#     ('BZ', 'Belize'),
#     ('BJ', 'Benin'),
#     ('BM', 'Bermuda'),
#     ('BT', 'Bhutan'),
#     ('BO', 'Bolivia'),
#     ('BA', 'Bosnia and Herzegovina'),
#     ('BW', 'Botswana'),
#     ('BV', 'Bouvet Island'),
#     ('BR', 'Brazil'),
#     ('IO', 'British Indian Ocean Territory'),
#     ('BN', 'Brunei Darussalam'),
#     ('BG', 'Bulgaria'),
#     ('BF', 'Burkina Faso'),
#     ('BI', 'Burundi'),
#     ('KH', 'Cambodia'),
#     ('CM', 'Cameroon'),
#     ('CA', 'Canada'),
#     ('CV', 'Cape Verde'),
#     ('KY', 'Cayman Islands'),
#     ('CF', 'Central African Republic'),
#     ('TD', 'Chad'),
#     ('CL', 'Chile'),
#     ('CN', 'China'),
#     ('CX', 'Christmas Island'),
#     ('CC', 'Cocos (Keeling) Islands'),
#     ('CO', 'Colombia'),
#     ('KM', 'Comoros'),
#     ('CG', 'Congo'),
#     ('CD', 'Congo, The Democratic Republic of the'),
#     ('CK', 'Cook Islands'),
#     ('CR', 'Costa Rica'),
#     ('CI', 'Cote d\'Ivoire'),
#     ('HR', 'Croatia'),
#     ('CU', 'Cuba'),
#     ('CY', 'Cyprus'),
#     ('CZ', 'Czech Republic'),
#     ('DK', 'Denmark'),
#     ('DJ', 'Djibouti'),
#     ('DM', 'Dominica'),
#     ('DO', 'Dominican Republic'),
#     ('EC', 'Ecuador'),
#     ('EG', 'Egypt'),
#     ('SV', 'El Salvador'),
#     ('GQ', 'Equatorial Guinea'),
#     ('ER', 'Eritrea'),
#     ('EE', 'Estonia'),
#     ('ET', 'Ethiopia'),
#     ('FK', 'Falkland Islands (Malvinas)'),
#     ('FO', 'Faroe Islands'),
#     ('FJ', 'Fiji'),
#     ('FI', 'Finland'),
#     ('FR', 'France'),
#     ('GF', 'French Guiana'),
#     ('PF', 'French Polynesia'),
#     ('TF', 'French Southern Territories'),
#     ('GA', 'Gabon'),
#     ('GM', 'Gambia'),
#     ('GE', 'Georgia'),
#     ('DE', 'Germany'),
#     ('GH', 'Ghana'),
#     ('GI', 'Gibraltar'),
#     ('GR', 'Greece'),
#     ('GL', 'Greenland'),
#     ('GD', 'Grenada'),
#     ('GP', 'Guadeloupe'),
#     ('GU', 'Guam'),
#     ('GT', 'Guatemala'),
#     ('GG', 'Guernsey'),
#     ('GN', 'Guinea'),
#     ('GW', 'Guinea-Bissau'),
#     ('GY', 'Guyana'),
#     ('HT', 'Haiti'),
#     ('HM', 'Heard Island and McDonald Islands'),
#     ('VA', 'Holy See (Vatican City State)'),
#     ('HN', 'Honduras'),
#     ('HK', 'Hong Kong'),
#     ('HU', 'Hungary'),
#     ('IS', 'Iceland'),
#     ('IN', 'India'),
#     ('ID', 'Indonesia'),
#     ('IR', 'Iran, Islamic Republic of'),
#     ('IQ', 'Iraq'),
#     ('IE', 'Ireland'),
#     ('IM', 'Isle of Man'),
#     ('IL', 'Israel'),
#     ('IT', 'Italy'),
#     ('JM', 'Jamaica'),
#     ('JP', 'Japan'),
#     ('JE', 'Jersey'),
#     ('JO', 'Jordan'),
#     ('KZ', 'Kazakhstan'),
#     ('KE', 'Kenya'),
#     ('KI', 'Kiribati'),
#     ('KP', 'Korea, Democratic People\'s Republic of'),
#     ('KR', 'Korea, Republic of'),
#     ('KW', 'Kuwait'),
#     ('KG', 'Kyrgyzstan'),
#     ('LA', 'Lao People\'s Democratic Republic'),
#     ('LV', 'Latvia'),
#     ('LB', 'Lebanon'),
#     ('LS', 'Lesotho'),
#     ('LR', 'Liberia'),
#     ('LY', 'Libyan Arab Jamahiriya'),
#     ('LI', 'Liechtenstein'),
#     ('LT', 'Lithuania'),
#     ('LU', 'Luxembourg'),
#     ('MO', 'Macao'),
#     ('MK', 'Macedonia, The Former Yugoslav Republic of'),
#     ('MG', 'Madagascar'),
#     ('MW', 'Malawi'),
#     ('MY', 'Malaysia'),
#     ('MV', 'Maldives'),
#     ('ML', 'Mali'),
#     ('MT', 'Malta'),
#     ('MH', 'Marshall Islands'),
#     ('MQ', 'Martinique'),
#     ('MR', 'Mauritania'),
#     ('MU', 'Mauritius'),
#     ('YT', 'Mayotte'),
#     ('MX', 'Mexico'),
#     ('FM', 'Micronesia, Federated States of'),
#     ('MD', 'Moldova'),
#     ('MC', 'Monaco'),
#     ('MN', 'Mongolia'),
#     ('ME', ('Montenegro')),
#     ('MS', ('Montserrat')),
#     ('MA', ('Morocco')),
#     ('MZ', ('Mozambique')),
#     ('MM', ('Myanmar')),
#     ('NA', ('Namibia')),
#     ('NR', ('Nauru')),
#     ('NP', ('Nepal')),
#     ('NL', ('Netherlands')),
#     ('AN', 'Netherlands Antilles'),
#     ('NC', ('New Caledonia')),
#     ('NZ', ('New Zealand')),
#     ('NI', ('Nicaragua')),
#     ('NE', ('Niger')),
#     ('NG', ('Nigeria')),
#     ('NU', ('Niue')),
#     ('NF', ('Norfolk Island')),
#     ('MP', ('Northern Mariana Islands')),
#     ('NO', ('Norway')),
#     ('OM', 'Oman'),
#     ('PK', 'Pakistan'),
#     ('PW', 'Palau'),
#     ('PS', 'Palestinian Territory, Occupied'),
#     ('PA', 'Panama'),
#     ('PG', 'Papua New Guinea'),
#     ('PY', 'Paraguay'),
#     ('PE', 'Peru'),
#     ('PH', 'Philippines'),
#     ('PN', 'Pitcairn'),
#     ('PL', 'Poland'),
#     ('PT', 'Portugal'),
#     ('PR', 'Puerto Rico'),
#     ('QA', 'Qatar'),
#     ('RE', 'Reunion'),
#     ('RO', 'Romania'),
#     ('RU', 'Russian Federation'),
#     ('RW', 'Rwanda'),
#     ('BL', 'Saint Barthelemy'),
#     ('SH', 'Saint Helena'),
#     ('KN', 'Saint Kitts and Nevis'),
#     ('LC', 'Saint Lucia'),
#     ('MF', 'Saint Martin'),
#     ('PM', 'Saint Pierre and Miquelon'),
#     ('VC', 'Saint Vincent and the Grenadines'),
#     ('WS', 'Samoa'),
#     ('SM', 'San Marino'),
#     ('ST', 'Sao Tome and Principe'),
#     ('SA', 'Saudi Arabia'),
#     ('SN', "Senegal"),
#     ('RS', 'Serbia'),
#     ('SC', 'Seychelles'),
#     ('SL', 'Sierra Leone'),
#     ('SG', 'Singapore'),
#     ('SK', 'Slovakia'),
#     ('SI', 'Slovenia'),
#     ('SB', 'Solomon Islands'),
#     ('SO', 'Somalia'),
#     ('ZA', 'South Africa'),
#     ('GS', 'South Georgia and the South Sandwich Islands'),
#     ('ES', 'Spain'),
#     ('LK', 'Sri Lanka'),
#     ('SD', 'Sudan'),
#     ('SR', 'Suriname'),
#     ('SJ', 'Svalbard and Jan Mayen'),
#     ('SZ', 'Swaziland'),
#     ('SE', 'Sweden'),
#     ('CH', 'Switzerland'),
#     ('SY', 'Syrian Arab Republic'),
#     ('TW', 'Taiwan, Province of China'),
#     ('TJ', 'Tajikistan'),
#     ('TZ', 'Tanzania, United Republic of'),
#     ('TH', 'Thailand'),
#     ('TL', 'Timor-Leste'),
#     ('TG', 'Togo'),
#     ('TK', 'Tokelau'),
#     ('TO', 'Tonga'),
#     ('TT', 'Trinidad and Tobago'),
#     ('TN', 'Tunisia'),
#     ('TR', 'Turkey'),
#     ('TM', 'Turkmenistan'),
#     ('TC', 'Turks and Caicos Islands'),
#     ('TV', 'Tuvalu'),
#     ('UG', 'Uganda'),
#     ('UA', 'Ukraine'),
#     ('AE', 'United Arab Emirates'),
#     ('US', 'United States'),
#     ('UM', 'United States Minor Outlying Islands'),
#     ('UY', 'Uruguay'),
#     ('UZ', 'Uzbekistan'),
#     ('VU', 'Vanuatu'),
#     ('VE', 'Venezuela'),
#     ('VN', 'Viet Nam'),
#     ('VG', 'Virgin Islands, British'),
#     ('VI', 'Virgin Islands, U.S.'),
#     ('WF', 'Wallis and Futuna'),
#     ('EH', 'Western Sahara'),
#     ('YE', 'Yemen'),
#     ('ZM', 'Zambia'),
#     ('ZW', 'Zimbabwe'),
# )


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
    # country = models.CharField(max_length=30, blank=True, null=True, choices=COUNTRIES)
    country = CountryField(blank_label='Select country of practice')
    city = models.CharField(max_length=30, blank=True, null=True)
    hospital = models.CharField(max_length=30, blank=True, null=True)
    work_number = models.CharField(max_length=30, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars", default='avatars/none/default.jpeg', height_field=None,
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
        template = get_template('invitation/invitation_email.html')
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

