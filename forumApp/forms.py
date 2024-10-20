from django import forms
from django.core.exceptions import ValidationError

from forumApp.posts.choices import LanguageChoice
from forumApp.posts.mixins import DisableFieldsMixin
from forumApp.posts.models import Post


class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        field = '__all__'

        error_messages = {
            'title': {
                'required': 'Please enter the title of your post.',
                'max_length': f'Title is too long. Max length is {Post.TITLE_MAX_LENGTH} characters.'
            },
            'author': {
                'required': 'Please enter an author name.'
            }
        }

    def clean_author(self):
        author = self.cleaned_data.get('author')

        if not author[0].isupper():
            raise ValidationError('Author name should start with capital letter!')

        return author

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title and content and title in content:
            raise ValidationError('The post title cannot be included in the post content!')

        return cleaned_data

    def save(self, commit=True):
        post = super().save(commit=False)
        post.title = post.title.capitalize()

        if commit:
            post.save()

        return post


class PostCreateForm(PostBaseForm):
    pass


class PostEditForm(PostBaseForm, DisableFieldsMixin):
    disabled_fields = ('title',)
    pass


class PostDeleteForm(PostBaseForm, DisableFieldsMixin):
    pass


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
