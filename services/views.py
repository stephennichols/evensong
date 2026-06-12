from django.http import HttpResponse
from django.template import loader

from .models import Service

def index(request):
    latest_services = Service.objects.all().order_by("-startDateTime")[:5]
    template = loader.get_template("services/index.html")
    context = {"latest_services": latest_services}
    return HttpResponse(template.render(context, request))

def detail(request, service_id):
    service = (Service.objects
               .filter(id=service_id)
               .select_related("venue")
               .first()
               )
    template = loader.get_template("services/details.html")
    context = {"service": service}
    return HttpResponse(template.render(context, request))
