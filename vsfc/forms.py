from django import forms


class UploadFileForm(forms.Form):
    vocal_sequence_file = forms.FileField()
