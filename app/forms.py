from django import forms


class NameForm(forms.Form):
    your_name = forms.CharField(label='Search', max_length=100)
