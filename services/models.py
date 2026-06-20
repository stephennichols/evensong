from django.db import models
from django.core import serializers
import json

class ExternalUrl(models.Model):
    urlType = models.CharField(max_length=50)
    value = models.URLField(max_length=255)
    lastVerified =  models.DateTimeField()
    def __str__(self):
        return self.value
    def as_public_json(self):
        return json.dumps(self.as_json())

class Venue(models.Model):
    name = models.CharField(max_length=50)
    townCity = models.CharField(max_length=50)
    mapUrl = models.OneToOneField(ExternalUrl, on_delete=models.CASCADE, related_name="venueMap", blank=True, null=True)
    wikiUrl = models.OneToOneField(ExternalUrl, on_delete=models.CASCADE, related_name="venueWikiUrl", blank=True, null=True)
    websiteUrl = models.OneToOneField(ExternalUrl, on_delete=models.CASCADE, related_name="venueWebsite", blank=True, null=True)
    def __str__(self):
        return self.name
    def as_public_json(self):
        return json.dumps(self.as_json())

class Musician(models.Model):
    fullName = models.CharField(max_length=255)
    knownAs = models.CharField(max_length=255, blank=True, null=True)
    wikiUrl = models.OneToOneField(ExternalUrl, on_delete=models.CASCADE, related_name="musicianWikiUrl", blank=True, null=True)
    websiteUrl = models.OneToOneField(ExternalUrl, on_delete=models.CASCADE, related_name="musicianWebsite", blank=True, null=True)
    def __str__(self):
        return self.knownAs if self.knownAs != "" and self.knownAs is not None else self.fullName
    def as_json(self):
        return {
            'fullName': self.fullName,
            'knownAs': self.knownAs,
            'wikiUrl': self.wikiUrl.value if self.wikiUrl is not None else None,
            'websiteUrl': self.websiteUrl.value if self.websiteUrl is not None else None,
        }
    def as_public_json(self):
        return json.dumps(self.as_json())

class Choir(models.Model):
    name = models.CharField(max_length=255)
    homeVenue = models.OneToOneField(Venue, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.name
    def as_public_json(self):
        return json.dumps(self.as_json())

class Anthem(models.Model):
    title = models.CharField(max_length=255)
    composer = models.ForeignKey(Musician, on_delete=models.CASCADE)
    knownAs = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.knownAs if self.knownAs != "" and self.knownAs is not None else self.title
    def as_json(self):
        return {
            'title': self.title,
            'composer': self.composer.knownAs if self.composer.knownAs != "" and self.composer.knownAs is not None else self.composer.fullName,
            'knownAs': self.knownAs,
        }
    def as_public_json(self):
        return json.dumps(self.as_json())

class Canticles(models.Model):
    description = models.CharField(max_length=255)
    composer = models.ForeignKey(Musician, on_delete=models.CASCADE)
    knownAs = models.CharField(max_length=255)
    def __str__(self):
        return self.knownAs
    def as_json(self):
        return {
            'description': self.description,
            'composer': self.composer.knownAs if self.composer.knownAs != "" and self.composer.knownAs is not None else self.composer.fullName,
            'knownAs': self.knownAs
        }
    def as_public_json(self):
        return json.dumps(self.as_json())

class Responses(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    composer = models.ForeignKey(Musician, on_delete=models.CASCADE)
    knownAs = models.CharField(max_length=255)
    def __str__(self):
        return self.knownAs
    def as_json(self):
        return {
            'title': self.title,
            'composer': self.composer.knownAs if self.composer.knownAs != "" and self.composer.knownAs is not None else self.composer.fullName,
            'knownAs': self.knownAs
        }
    def as_public_json(self):
        return json.dumps(self.as_json())

class MusicList(models.Model):
    responses = models.ForeignKey(Responses, on_delete=models.CASCADE)
    canticles = models.ForeignKey(Canticles, on_delete=models.CASCADE)
    anthem = models.ForeignKey(Anthem, on_delete=models.CASCADE, unique=False)
    def __str__(self):
        return self.responses.knownAs + " Responses, " + self.canticles.knownAs + ", " + self.anthem.__str__()
    def as_json(self):
        return {
            'responses': self.responses.knownAs,
            'canticles': self.canticles.knownAs,
            'anthem': self.anthem.as_json(),
        }
    def as_public_json(self):
        return json.dumps(self.as_json())

class Service(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    startDateTime = models.DateTimeField()
    conductor = models.ForeignKey(Musician, on_delete=models.CASCADE, blank=True, null=True)
    choir = models.ForeignKey(Choir, on_delete=models.CASCADE, related_name="serviceChoir", blank=True, null=True)
    musicList = models.OneToOneField(MusicList, on_delete=models.CASCADE)
    def __str__(self):
        return self.venue.name + " " + self.startDateTime.strftime('%d %h %Y %H:%M')
    def as_json(self):
        return {
            'venue': self.venue.name,
            'startDateTime': self.startDateTime.strftime('%Y-%m-%d %H:%M'),
            'conductor': self.conductor.fullName if self.conductor is not None else None,
            'choir': self.choir.name if self.choir is not None else None,
            'musicList': self.musicList.as_json(),
        }
    def as_public_json(self):
        return json.dumps(self.as_json())
