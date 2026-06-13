from django.http import HttpResponse
from django.template import loader
from django.db.models import Q

from .models import Service, Venue


def index(request):
    latest_services = Service.objects.all().order_by("-startDateTime")[:5]
    template = loader.get_template("services/pages/index.html")
    context = {"services": latest_services, "heading": "Upcoming services"}
    return HttpResponse(template.render(context, request))

def detail(request, service_id):
    service = (Service.objects
               .filter(id=service_id)
               .select_related("venue")
               .first()
               )
    template = loader.get_template("services/pages/serviceDetails.html")
    context = {"service": service}
    return HttpResponse(template.render(context, request))

def responsesIndex(request, responses_id):
    services = (Service.objects
               .filter(musicList__responses_id=responses_id)
               )
    template = loader.get_template("services/pages/index.html")
    context = {"services": services, "heading": "Services containing these responses"}
    return HttpResponse(template.render(context, request))

def canticlesIndex(request, canticles_id):
    services = (Service.objects
                .filter(musicList__canticles_id=canticles_id)
                )
    template = loader.get_template("services/pages/index.html")
    context = {"services": services, "heading": "Services containing these canticles"}
    return HttpResponse(template.render(context, request))

def anthemIndex(request, anthem_id):
    services = (Service.objects
                .filter(musicList__anthem_id=anthem_id)
                )
    template = loader.get_template("services/pages/index.html")
    context = {"services": services, "heading": "Services containing this anthem"}
    return HttpResponse(template.render(context, request))

def musicianIndex(request, musician_id):
    services = (Service.objects
                .filter(
        Q(conductor_id=musician_id) |
        Q(musicList__responses__composer_id=musician_id) |
        Q(musicList__canticles__composer_id=musician_id) |
        Q(musicList__anthem__composer_id=musician_id)
    ))
    template = loader.get_template("services/pages/index.html")
    context = {"services": services, "heading": "Services featuring this musician"}
    return HttpResponse(template.render(context, request))

def venueIndex(request, venue_id):
    services = (Service.objects
                .filter(venue_id=venue_id)
                )
    template = loader.get_template("services/pages/index.html")
    context = {"services": services, "heading": "Services at this venue"}
    return HttpResponse(template.render(context, request))

