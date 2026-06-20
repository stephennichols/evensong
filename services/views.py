from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.db.models import Q

from .models import Service, Musician, Responses, Canticles
from .forms import MusicianForm, ResponsesForm, CanticlesForm

def index(request):
    latest_services = Service.objects.all().order_by("-startDateTime")[:5]
    template = loader.get_template("services/pages/index.html")
    context = {"services": latest_services, "heading": "Upcoming services:"}
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
    responses = (Responses.objects
               .filter(id=responses_id)
               .first()
               )
    template = loader.get_template("services/pages/responsesIndex.html")
    context = {
        "services": services,
        "responses": responses,
        "heading": "Services containing these responses:"
    }
    return HttpResponse(template.render(context, request))

def responsesAdd(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ResponsesForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            knownAs = form.cleaned_data.get("knownAs")
            title = form.cleaned_data.get("title")
            if Responses.objects.filter(knownAs=knownAs).exists():
                return HttpResponse("400 Bad Request These responses already exist")
            if not Musician.objects.filter(knownAs=knownAs).exists():
                #TODO Auto create this musician
                return HttpResponse("400 Bad Request Please add this composer first")
            musician_id = Musician.objects.get(knownAs=knownAs).pk
            r = Responses(title=title, composer_id=musician_id, knownAs=knownAs)
            r.save()
            if Responses.objects.filter(knownAs=knownAs).exists():
                new_id = Responses.objects.get(knownAs=knownAs).pk.__str__()
                # redirect to a new URL:
                return HttpResponseRedirect("/services/responses/" + new_id + "/")
            return HttpResponse("500 Server Error There was an error saving the form. Please try again.")
        else:
            return HttpResponse("400 Bad Request There was an error with your form. Please try again.")
    else:
        return HttpResponse("405 Method Not Allowed")

def responsesList(request):
    responses = Responses.objects.all().order_by("knownAs")
    template = loader.get_template("services/pages/responsesList.html")
    context = {"responses": responses, "heading": "Responses"}
    return HttpResponse(template.render(context, request))

def canticlesIndex(request, canticles_id):
    services = (Service.objects
                .filter(musicList__canticles_id=canticles_id)
                )
    canticles = (Canticles.objects.filter(id=canticles_id).first())
    template = loader.get_template("services/pages/canticlesIndex.html")
    context = {
        "services": services,
        "canticles": canticles,
        "heading": "Services containing these canticles:"
    }
    return HttpResponse(template.render(context, request))

def canticlesAdd(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = CanticlesForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            knownAs = form.cleaned_data.get("knownAs")
            description = form.cleaned_data.get("description")
            composerName = form.cleaned_data.get("composerName")
            if Canticles.objects.filter(knownAs=knownAs).exists():
                return HttpResponse("400 Bad Request These canticles already exist: " + knownAs)
            if not Musician.objects.filter(knownAs=composerName).exists():
                #TODO Auto create this musician
                return HttpResponse("400 Bad Request Please add this composer first: " + composerName)
            musician_id = Musician.objects.get(knownAs=composerName).pk
            r = Canticles(description=description, composer_id=musician_id, knownAs=knownAs)
            r.save()
            if Canticles.objects.filter(knownAs=knownAs).exists():
                new_id = Canticles.objects.get(knownAs=knownAs).pk.__str__()
                # redirect to a new URL:
                return HttpResponseRedirect("/services/canticles/" + new_id + "/")
            return HttpResponse("500 Server Error There was an error saving the form. Please try again.")
        else:
            return HttpResponse("400 Bad Request There was an error with your form. Please try again.")
    else:
        return HttpResponse("405 Method Not Allowed")

def canticlesList(request):
    canticles = Canticles.objects.all().order_by("knownAs")
    template = loader.get_template("services/pages/canticlesList.html")
    context = {"canticles": canticles, "heading": "Canticles"}
    return HttpResponse(template.render(context, request))

def anthemIndex(request, anthem_id):
    services = (Service.objects
                .filter(musicList__anthem_id=anthem_id)
                )
    template = loader.get_template("services/pages/index.html")
    context = {"services": services, "heading": "Services containing this anthem:"}
    return HttpResponse(template.render(context, request))

def musicianAdd(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = MusicianForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            fullName = form.cleaned_data.get("fullName")
            knownAs = form.cleaned_data.get("knownAs")
            if Musician.objects.filter(fullName=fullName).exists():
                return HttpResponse("400 Bad Request This musician already exists")
            if Musician.objects.filter(knownAs=knownAs).exists():
                return HttpResponse("400 Bad Request This musician already exists")
            m = Musician(fullName=fullName, knownAs=knownAs)
            m.save()
            if Musician.objects.filter(fullName=fullName).exists():
                new_id = Musician.objects.get(fullName=fullName).pk.__str__()
                # redirect to a new URL:
                return HttpResponseRedirect("/services/musicians/" + new_id + "/")
            return HttpResponse("500 Server Error There was an error saving the form. Please try again.")
        else:
            return HttpResponse("400 Bad Request There was an error with your form. Please try again.")
    else:
        return HttpResponse("405 Method Not Allowed")

def musicianIndex(request, musician_id):
    services = (Service.objects
                .filter(
        Q(conductor_id=musician_id) |
        Q(musicList__responses__composer_id=musician_id) |
        Q(musicList__canticles__composer_id=musician_id) |
        Q(musicList__anthem__composer_id=musician_id)
    ))
    musician = (Musician.objects.filter(id=musician_id).first())
    responses_by_composer = Responses.objects.filter(composer_id=musician_id).order_by("knownAs")
    canticles_by_composer = Canticles.objects.filter(composer_id=musician_id).order_by("knownAs")
    template = loader.get_template("services/pages/musicianIndex.html")
    context = {
        "services": services,
        "musician": musician,
        "responses_by_composer": responses_by_composer,
        "canticles_by_composer": canticles_by_composer,
        "heading": "Services featuring this musician:"}
    return HttpResponse(template.render(context, request))

def musicianList(request):
    musicians = Musician.objects.all().order_by("knownAs")
    template = loader.get_template("services/pages/musicianList.html")
    context = {"musicians": musicians, "heading": "Musicians"}
    return HttpResponse(template.render(context, request))

def venueIndex(request, venue_id):
    services = (Service.objects
                .filter(venue_id=venue_id)
                )
    template = loader.get_template("services/pages/index.html")
    context = {"services": services, "heading"  : "Services at this venue:"}
    return HttpResponse(template.render(context, request))

