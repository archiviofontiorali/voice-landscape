from django import forms


class UploadAudioForm(forms.Form):
    audio = forms.FileField()
