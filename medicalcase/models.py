import datetime
from django.db import models
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from userprofile.models import Doctor
from autoslug import AutoSlugField
from multiselectfield import MultiSelectField


GENDER = (('Female', 'Female'), ('Male', 'Male'), ('Others', 'Others'))

PURPOSE = (('I need help to arrive at diagnosis', 'I need help to arrive at diagnosis'),
           ('Interesting case, a lot to learn', 'Interesting case, a lot to learn'),
           ('Rare case', 'Rare case'), ('Personal write up to improve skill', 'Personal write up to improve skill'))


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



class MedicalCaseCategory(models.Model):
    name = models.CharField(max_length=200, blank=False, default="General Medicine ")
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Medical Case Categories"

    def __str__(self):
        return self.name


class MedicalCase(models.Model):
    title = models.CharField(max_length=200)
    chief_complaint = models.CharField(max_length=200)
    purpose = MultiSelectField(choices=PURPOSE, verbose_name="Reason for sharing medical case")
    patient_age = models.CharField(max_length=200)
    patient_gender = models.CharField(max_length=6, choices=GENDER, default='Female')
    patient_country_of_origin = models.CharField(max_length=200, blank=True, null=True, choices=COUNTRIES)
    history_of_present_illness = models.TextField()
    medical_history = models.TextField()
    surgical_history = models.TextField()
    social_history = models.TextField()
    family_history = models.TextField()
    allergies = models.TextField()
    medications = models.TextField()
    review_of_systems = models.TextField()
    physical_examination = models.TextField()
    diagnostic_tests = models.TextField()
    medical_case_category = models.ManyToManyField(MedicalCaseCategory)
    any_other_details = models.TextField()
    #slug = AutoSlugField(null=True, default=None, unique=True, populate_from='title', unique_with='created_at')
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    doctor = models.ForeignKey(Doctor, models.DO_NOTHING, blank=False, null=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Medical Cases"

    @classmethod
    def list_medical_cases(cls):
        return cls.objects.all()

    @classmethod
    def weekly_top_five_medical_case(cls):
        date_diff = datetime.datetime.now() - datetime.timedelta(days=7)
        return cls.objects.filter(created_at__range=(date_diff, datetime.datetime.now())).order_by('-created_at')[:5]

    @classmethod
    def send_medical_cases(cls, subject_medical_case, context, registered_doctor):
        subject = subject_medical_case.title
        message = render_to_string('medicalcase/emails/medical_case_email_update.html', context)
        to_email1 = registered_doctor.user.email
        email = EmailMessage(subject, message, to=[to_email1])
        email.content_subtype = "html"
        email.send()


class Photo(models.Model):
    diagnotic_image = models.ImageField(upload_to="medical_cases", height_field=None, width_field=None, blank=True, null=True)
    medical_case = models.ForeignKey(MedicalCase)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Photos"


class Comment(models.Model):
    comment_content = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    medical_case = models.ForeignKey(MedicalCase)
    doctor = models.ForeignKey(Doctor, related_name="doctor_comments")

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Comments"


class Reply(models.Model):
    reply_content = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    parent_comment_id = models.ForeignKey(Comment)
    medical_case = models.ForeignKey(MedicalCase)
    doctor = models.ForeignKey(Doctor, related_name="doctor_replies")

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Replies"

