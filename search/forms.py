from django import forms


class SearchForm(forms.Form):

    GENDER_CHOICES = (
        ('', 'Select Gender'),
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    )

    search = forms.CharField(required=False)
    city = forms.CharField(required=False)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select, required=False)
    age_more_than = forms.IntegerField(required=False)
    age_less_than = forms.IntegerField(required=False)
