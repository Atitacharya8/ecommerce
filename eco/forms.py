from django import forms

from . import models


class ReviewForm(forms.ModelForm):
    class Meta:
        fields=["rate","review"]
        model=models.Review