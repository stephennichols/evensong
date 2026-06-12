from django.db import models

class ExternalUrl(models.Model):
    urlType = models.CharField(max_length=50)
    value = models.CharField(max_length=255)
    lastVerified =  models.DateTimeField()
    def __str__(self):
        return self.value

class Venue(models.Model):
    name = models.CharField(max_length=50)
    townCity = models.CharField(max_length=50)
    map = models.ForeignKey(ExternalUrl, on_delete=models.CASCADE, related_name="venueMap", blank=True, null=True)
    wikiUrl = models.ForeignKey(ExternalUrl, on_delete=models.CASCADE, related_name="venueWikiUrl", blank=True, null=True)
    def __str__(self):
        return self.name

class Musician(models.Model):
    fullName = models.CharField(max_length=255)
    knownAs = models.CharField(max_length=255, blank=True, null=True)
    wikiUrl = models.ForeignKey(ExternalUrl, on_delete=models.CASCADE, related_name="musicianWikiUrl", blank=True, null=True)
    def __str__(self):
        return self.knownAs if self.knownAs != "" and self.knownAs is not None else self.fullName

class Choir(models.Model):
    name = models.CharField(max_length=255)
    homeVenue = models.ForeignKey(Venue, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.name

class Anthem(models.Model):
    title = models.CharField(max_length=255)
    composer = models.ForeignKey(Musician, on_delete=models.CASCADE)
    knownAs = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.knownAs if self.knownAs != "" and self.knownAs is not None else self.title

class Canticles(models.Model):
    description = models.CharField(max_length=255)
    composer = models.ForeignKey(Musician, on_delete=models.CASCADE)
    knownAs = models.CharField(max_length=255)

class Responses(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    composer = models.ForeignKey(Musician, on_delete=models.CASCADE)
    knownAs = models.CharField(max_length=255)

class MusicList(models.Model):
    responses = models.ForeignKey(Responses, on_delete=models.CASCADE)
    canticles = models.ForeignKey(Canticles, on_delete=models.CASCADE)
    anthem = models.ForeignKey(Anthem, on_delete=models.CASCADE)
    def __str__(self):
        return self.responses.knownAs + " Responses, " + self.canticles.knownAs + ", " + self.anthem.__str__()

class Service(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="serviceVenue")
    startDateTime = models.DateTimeField()
    conductor = models.ForeignKey(Musician, on_delete=models.CASCADE, blank=True, null=True)
    choir = models.ForeignKey(Choir, on_delete=models.CASCADE, related_name="serviceChoir", blank=True, null=True)
    musicList = models.ForeignKey(MusicList, on_delete=models.CASCADE)
    def __str__(self):
        return self.venue.name + " " + self.startDateTime.strftime('%d %h %Y %H:%M')

