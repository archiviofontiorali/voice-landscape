from django import forms


class UploadAudioForm(forms.Form):
    audio = forms.FileField()
    media_type = forms.CharField(max_length=100)
