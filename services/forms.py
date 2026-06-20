from django import forms


class MusicianForm(forms.Form):
    fullName = forms.CharField(label="Full name", max_length=255)
    knownAs = forms.CharField(label="Known as", max_length=255)

class ResponsesForm(forms.Form):
    title = forms.CharField(label="Title", max_length=255, required=False)
    composerName = forms.CharField(label="Composer name", max_length=255)
    knownAs = forms.CharField(label="Known as", max_length=255)
