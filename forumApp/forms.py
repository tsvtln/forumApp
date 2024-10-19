from django import forms

from forumApp.posts.choices import LanguageChoice
from forumApp.posts.models import Post


class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        field = '__all__'


class PostCreateForm(PostBaseForm):
    pass


class PostEditForm(PostBaseForm):
    pass


class PostDeleteForm(PostBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].disabled = True


class SearchForm(forms.Form):
    query = forms.CharField(
        label='',
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search for a post...',
            }
        )
    )

#
# class PostForm(forms.Form):
#     title = forms.CharField(
#         max_length=100,
#     )
#
#     content = forms.CharField(
#         widget=forms.Textarea,
#     )
#
#     author = forms.CharField(
#         max_length=30,
#     )
#
#     created_at = forms.DateTimeField()
#
#     languages = forms.ChoiceField(
#         choices=LanguageChoice.choices
#     )

# class PersonForm(forms.Form):
#
#     STATUS_CHOICE = (
#         (1, 'Draft'),
#         (2, 'Published'),
#         (3, 'Archived'),
#     )
#
#     person_name = forms.CharField(
#         label="Add person name",
#         max_length=10,
#         widget=forms.TextInput(attrs={'placeholder': 'Person name'})
#     )
#     age = forms.IntegerField(
#         label="Add person age",
#         widget=forms.TextInput(attrs={'placeholder': 'Person age'})
#     )
#
#     date_of_registration = forms.DateTimeField(
#         widget=forms.DateInput(attrs={'placeholder': 'DD/MM/YYYY'}),
#         help_text='Enter Registration Date in the form of Date/Month/Year'
#     )
#
#     # is_lecturer = forms.BooleanField()
#
#     # status = forms.ChoiceField(
#     #     choices=STATUS_CHOICE
#     # )
#
#     status = forms.IntegerField(
#         widget=forms.Select(choices=STATUS_CHOICE),
#     )
#
#     email = forms.CharField(
#         widget=forms.EmailInput(attrs={'placeholder': 'example@domain.com'}),
#     )
