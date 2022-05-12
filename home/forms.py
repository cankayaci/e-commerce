from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=110)
    catid = forms.IntegerField()
