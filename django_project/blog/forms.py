from django import forms
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Tag, Post

class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['title', 'slug']


    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Create is not possible as slug')


        if Tag.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('Not possible, already exist')

        return new_slug


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'tag', 'author']

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Sorry, this slug prohibited for adding')

        return new_slug

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']



