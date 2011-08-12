import django.forms

class CreateFileForm(django.forms.Form):
    syncedFile = django.forms.FileField(label = "File to synchronize")

class UploadNewVersionForm(django.forms.Form):
    syncedFile = django.forms.FileField(label = "Newer version of the file")

class TagFileForm(django.forms.Form):
    tagName = django.forms.CharField(label = "Tagname")
