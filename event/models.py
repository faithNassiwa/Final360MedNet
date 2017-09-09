from django.db import models

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=100)
    continent = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @classmethod
    def add_country(cls, name, continent):
        cls.objects.create(name=name, continent=continent)


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @classmethod
    def add_city(cls, name, country):
        cls.objects.create(name=name, country=country)


class EventType(models.Model):
    name = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class EventTopic(models.Model):
    name = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=100)
    venue = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    country = models.ForeignKey(Country)
    city = models.ForeignKey(City)
    start = models.DateTimeField()
    end = models.DateTimeField()
    image = models.ImageField(upload_to="events/images", default='events/images/default.jpg', height_field=None,
                              width_field=None, blank=True, null=True)
    description = models.TextField(max_length=5000)
    organiser = models.CharField(max_length=200, null=True, blank=True)
    organiser_details = models.TextField(2000, null=True, blank=True)
    facebook_link = models.URLField(max_length=200, null=True, blank=True)
    twitter_link = models.URLField(max_length=200, null=True, blank=True)
    price = models.CharField(max_length=100)
    type = models.ForeignKey(EventType)
    topic = models.ForeignKey(EventTopic)
    tags = models.CharField(max_length=500, null=True, blank=True)
    resource = models.FileField(upload_to="events/files", default='events/files/default.pdf', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @classmethod
    def get_event_by_id(cls, event_id):
        return cls.objects.get(pk=event_id)

    @classmethod
    def get_other_events(cls, event_id):
        return cls.objects.all().exclude(pk=event_id)


# scholarship models
class ScholarshipCategory(models.Model):
    name = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Scholarship(models.Model):
    title = models.CharField(max_length=200)
    deadline = models.DateTimeField()
    award_amount = models.CharField(max_length=100)
    description = models.TextField(max_length=5000, null=True, blank=True)
    category = models.ForeignKey(ScholarshipCategory)
    website = models.URLField(max_length=200)
    image = models.ImageField(upload_to="scholarships/images", default='scholarships/images/default.jpg', height_field=None,
                              width_field=None, blank=True, null=True)
    resource = models.FileField(upload_to="scholarships/files", blank=True, null=True)
    tags = models.CharField(max_length=200)

    def __str__(self):
        return self.title


# job model
class JobCategory(models.Model):
    name = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    title = models.CharField(max_length=100)
    deadline = models.DateTimeField()
    description = models.TextField(max_length=5000, null=True, blank=True)
    category = models.ForeignKey(JobCategory)
    website = models.URLField(max_length=200)
    image = models.ImageField(upload_to="jobs/images", default='jobs/images/default.jpg', height_field=None,
                              width_field=None, blank=True, null=True)
    resource = models.FileField(upload_to="jobs/files", blank=True, null=True)
    tags = models.CharField(max_length=200)

    def __str__(self):
        return self.title