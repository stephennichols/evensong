from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:service_id>/", views.detail, name="detail"),

    path("responses/", views.responsesList, name="responsesList"),
    path("responses/<int:responses_id>/", views.responsesIndex, name="responsesIndex"),
    path("responses/add", views.responsesAdd, name="responsesAdd"),
    path("canticles/", views.canticlesList, name="canticlesList"),
    path("canticles/<int:canticles_id>/", views.canticlesIndex, name="canticlesIndex"),
    path("canticles/add", views.canticlesAdd, name="canticlesAdd"),
    path("anthems/", views.anthemList, name="anthemList"),
    path("anthems/<int:anthem_id>/", views.anthemIndex, name="anthemIndex"),
    path("anthems/add", views.anthemAdd, name="anthemAdd"),

    path("musicians/", views.musicianList, name="musicianList"),
    path("musicians/<int:musician_id>/", views.musicianIndex, name="musicianIndex"),
    path("musicians/add", views.musicianAdd, name="musicianAdd"),
    path("venues/<int:venue_id>/", views.venueIndex, name="venueIndex"),
]