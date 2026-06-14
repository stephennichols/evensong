from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:service_id>/", views.detail, name="detail"),
    path("responses/<int:responses_id>/", views.responsesIndex, name="responsesIndex"),
    path("canticles/<int:canticles_id>/", views.canticlesIndex, name="canticlesIndex"),
    path("anthems/<int:anthem_id>/", views.anthemIndex, name="anthemIndex"),
    path("musicians/<int:musician_id>/", views.musicianIndex, name="musicianIndex"),
    path("musicians/add", views.musicianAdd, name="musicianAdd"),
    path("venues/<int:venue_id>/", views.venueIndex, name="venueIndex"),
]