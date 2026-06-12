from django.contrib import admin

from .models import Venue, Choir, Musician, ExternalUrl, Responses, Canticles, Anthem, Service, MusicList

admin.site.register(ExternalUrl)
admin.site.register(Venue)
admin.site.register(Choir)
admin.site.register(Musician)
admin.site.register(Anthem)
admin.site.register(Canticles)
admin.site.register(Responses)
admin.site.register(Service)
admin.site.register(MusicList)