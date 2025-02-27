from django import forms
from .models import PostModel, Comment, Contacts
from crispy_forms.layout import Layout, Field, Row, Column


class PostModelForm(forms.ModelForm):
       # Example of using ChoiceField
    OPTIONS = [
        ('', 'Select an Option'),
        ('Kenyan Politics', 'Kenyan Politics'),
        ('Kenyan Economy', 'Kenyan Economy'),
        ('Kenyan Health', 'Kenyan Health'),
        ('Kenyan Education', 'Kenyan Education'),
        ('Global Sports', 'Global Sports'),
        ('Global Politics', 'Global Politics'),
        ('Global Tech', 'Global Tech'),
    ]
    
    topic = forms.ChoiceField(choices=OPTIONS, required=True)
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'custom-class', 'placeholder': 'Enter title'}))
    content = forms.CharField(widget = forms.Textarea(attrs={'class': 'custom-textarea', 'rows': 4, 'placeholder': 'Post your content'}))    
    picture = forms.ImageField( required=False, widget=forms.ClearableFileInput(attrs={'class': 'custom-image', 'placeholder': 'Choose an Image'}))   
    class Meta:
        model = PostModel
        fields = ('topic','picture', 'title', 'content')


class CommentForm(forms.ModelForm):
    your_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'custom-class', 'placeholder': 'Enter your name'}))
    comment_on_the_post = forms.CharField(required=True, widget = forms.Textarea(attrs={'class': 'custom-textarea', 'rows': 2, 'placeholder': 'Write your comment'}))    
    class Meta:
        model = Comment
        fields = ('your_name','comment_on_the_post' )

class ContactForm(forms.ModelForm):
    message = forms.CharField(required=False, widget = forms.Textarea(attrs={'class': 'custom-textarea', 'rows': 2, 'placeholder': 'Write your Message'}))    
    class Meta:
        model = Contacts
        fields = ('your_name', 'your_email', 'subject', 'message')

class SearchForm(forms.ModelForm):
    query = forms.CharField(max_length=100, required=False, label='Search')
    topic = forms.CharField(max_length=100, required=False, label='Topic')
    author = forms.CharField(max_length=100, required=False, label='Author')
    title = forms.CharField(max_length=100, required=False, label='Title')