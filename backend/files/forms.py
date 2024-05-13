# files/forms.py

from django import forms
from .models import File

# defining a form for our model File
class FileForm(forms.ModelForm):
    class Meta:
        # specifying that it'll be based on File model
        model = File
        # only document field should appear in the form
        fields = ['document']
