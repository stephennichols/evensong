from django.http import HttpResponse
from django.template import loader

from .models import Service

def index(request):
    latest_services = Service.objects
    template = loader.get_template("services/index.html")
    context = {"latest_services": latest_services}
    return HttpResponse(template.render(context, request))

def detail(request, service_id):
    return HttpResponse("Hello. This is service %s." % service_id)
