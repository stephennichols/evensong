from django.db import models
from django.core import serializers
import json

class ExternalUrl(models.Model):
    urlType = models.CharField(max_length=50)
    value = models.URLField(max_length=255)
    lastVerified =  models.DateTimeField()
    def __str__(self):
        return self.value

class Venue(models.Model):
    name = models.CharField(max_length=50)
    townCity = models.CharField(max_length=50)
    mapUrl = models.OneToOneField(ExternalUrl, on_delete=models.CASCADE, related_name="venueMap", blank=True, null=True)
    wikiUrl = models.OneToOneField(ExternalUrl, on_delete=models.CASCADE, related_name="venueWikiUrl", blank=True, null=True)
    websiteUrl = models.OneToOneField(ExternalUrl, on_delete=models.CASCADE, related_name="venueWebsite", blank=True, null=True)
    def __str__(self):
        return self.name

class Musician(models.Model):
    fullName = models.CharField(max_length=255)
    knownAs = models.CharField(max_length=255, blank=True, null=True)
    wikiUrl = models.OneToOneField(ExternalUrl, on_delete=models.CASCADE, related_name="musicianWikiUrl", blank=True, null=True)
    def __str__(self):
        return self.knownAs if self.knownAs != "" and self.knownAs is not None else self.fullName

class Choir(models.Model):
    name = models.CharField(max_length=255)
    homeVenue = models.OneToOneField(Venue, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.name

class Anthem(models.Model):
    title = models.CharField(max_length=255)
    composer = models.OneToOneField(Musician, on_delete=models.CASCADE)
    knownAs = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.knownAs if self.knownAs != "" and self.knownAs is not None else self.title
    def as_json(self):
        return {
            'title': self.title,
            'composer': self.composer.knownAs if self.composer.knownAs != "" and self.composer.knownAs is not None else self.composer.fullName,
            'knownAs': self.knownAs,
        }

class Canticles(models.Model):
    description = models.CharField(max_length=255)
    composer = models.OneToOneField(Musician, on_delete=models.CASCADE)
    knownAs = models.CharField(max_length=255)
    def __str__(self):
        return self.knownAs

class Responses(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    composer = models.OneToOneField(Musician, on_delete=models.CASCADE)
    knownAs = models.CharField(max_length=255)
    def __str__(self):
        return self.knownAs

class MusicList(models.Model):
    responses = models.OneToOneField(Responses, on_delete=models.CASCADE)
    canticles = models.OneToOneField(Canticles, on_delete=models.CASCADE)
    anthem = models.ForeignKey(Anthem, on_delete=models.CASCADE, unique=False)
    def __str__(self):
        return self.responses.knownAs + " Responses, " + self.canticles.knownAs + ", " + self.anthem.__str__()
    def as_json(self):
        return {
            'responses': self.responses.knownAs,
            'canticles': self.canticles.knownAs,
            'anthem': self.anthem.as_json(),
        }

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
