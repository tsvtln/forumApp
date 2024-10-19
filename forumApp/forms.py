from django import forms


class PersonForm(forms.Form):

    STATUS_CHOICE = (
        (1, 'Draft'),
        (2, 'Published'),
        (3, 'Archived'),
    )

    person_name = forms.CharField(
        label="Add person name",
        max_length=10,
        widget=forms.TextInput(attrs={'placeholder': 'Person name'})
    )
    age = forms.IntegerField(
        label="Add person age",
        widget=forms.TextInput(attrs={'placeholder': 'Person age'})
    )

    date_of_registration = forms.DateTimeField(
        widget=forms.DateInput(attrs={'placeholder': 'DD/MM/YYYY'}),
        help_text='Enter Registration Date in the form of Date/Month/Year'
    )

    # is_lecturer = forms.BooleanField()

    # status = forms.ChoiceField(
    #     choices=STATUS_CHOICE
    # )

    status = forms.IntegerField(
        widget=forms.Select(choices=STATUS_CHOICE),
    )

    email = forms.CharField(
        widget=forms.EmailInput(attrs={'placeholder': 'example@domain.com'}),
    )
