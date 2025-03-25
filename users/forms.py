from django.contrib.auth.forms  import UserCreationForm
from django.contrib.auth.models import User
from .models import Author
from django import forms

# class SignUpForm(UserCreationForm):
#     profile_image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'custom-image', 'placeholder': 'Choose a profile Image'}))   
#     email =  forms.EmailField()

#     class Meta:
#         model = User
#         fields = ['profile_image','username', 'email', 'password1', 'password2']

#     # def save(self, commit=True):
#     #     # save the user object first
#     #     user = super().save(commit=False)
#     #     if commit:
#     #         user.save()

#     #     # save the Userprofile object with the user
#     #     user_profile = UserProfile(user=user, profile_picture=self.cleaned_data.get('profile_picture'))
#     #     if commit:
#     #         user_profile.save()
#     #     return user
#     def __init__(self, *args, **kwargs):
#         super(SignUpForm, self).__init__(*args, **kwargs)

#         for fieldname in ['username', 'email', 'password1', 'password2']:
#              self.fields[fieldname].help_text = None

class AuthorUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=100, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Set Password'}),
        required=True,
        min_length=8  # You can also specify a minimum length
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        required=True,
        min_length=8  # Same here, enforce minimum length if needed
    )

    class Meta:
        model = User
        fields = ['first_name', 'email', 'last_name', 'username', 'password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(attrs={'placeholder': 'Set Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})           
        }

    def __init__(self, *args, **kwargs):
        super(AuthorUserForm, self).__init__(*args, **kwargs)

        for fieldname in ['first_name','email', 'last_name','username', 'password1', 'password2']:
                self.fields[fieldname].help_text = None

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Check if passwords match
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data 

class AuthorForm(forms.ModelForm):
    address = forms.CharField(required=False)
    class Meta:
        model = Author
        fields = {'phone_number', 'address', 'profile_picture'}


# class AuthorProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ('user_name', 'email','profile_picture','phone_number')
class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=30)
    email = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email')
class ProfileUpdateForm(forms.ModelForm):
    phone_number = forms.IntegerField(required=False)
    profile_picture = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'custom-image', 'placeholder': 'Choose a profile Image'}))   
    brief_description = forms.CharField(required=False, widget = forms.Textarea(attrs={'class': 'custom-textarea', 'rows': 4, 'placeholder': 'Briefly decribe yourself'}))    
    class Meta:
        model = Author
        fields = ['profile_picture', 'phone_number', 'brief_description']