from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserUpdateForm, AuthorForm, AuthorUserForm, ProfileUpdateForm
from .models import Author
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User




# Create your views here.

def author_signup_view(request):
    userForm=AuthorUserForm()
    authorForm=AuthorForm()
    mydict={'userForm':userForm,'authorForm':authorForm}
    if request.method=='POST':
        userForm=AuthorUserForm(request.POST, request.FILES)
        authorForm=AuthorForm(request.POST,request.FILES)
        if userForm.is_valid() and authorForm.is_valid():
            my_user=userForm.save(commit=False)
            # my_user.set_password(my_user.password)
            my_user.save()
            author=authorForm.save(commit=False)
            author.user=my_user
            author.save()
            my_author_group = Group.objects.get_or_create(name='CUSTOMER')
            my_author_group[0].user_set.add(my_user)
            username = userForm.cleaned_data.get('username')
            messages.success(request, f"Your account has been successfully created {username}")
        return redirect('users-login')
    return render(request,'users/author_sign_up.html', context=mydict)

def is_author(user):
    return user.groups.filter(name='CUSTOMER').exists()

# def sign_up(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST, request.FILES)
#         if form.is_valid():
#             user_profile = form.save(commit=False)
#             user_profile.user = request.user
#             user_profile.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f"Your account has been successfully created {username}")
#             login(request, user_profile.user)
#             # return redirect('users-login')
#     else:
#         form = SignUpForm()
#     context = {
#         'form' : form,
#     }

#     return render(request, 'users/sign_up.html', context)

def customerhome(request):
    return render(request, 'users/customer-home.html')

@login_required
def profile(request):
    u_form = UserUpdateForm()
    p_form = ProfileUpdateForm()

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile_form.html', context)

def authorinfo(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Author, user=user)
    return render(request, 'users/author_info.html', {'profile': profile, 'user': user})

# @login_required
# def profile_view(request):
#     # Get the current user's profile
#     profile = UserProfile.objects.get(user=request.user)
#     return render(request, 'user_profile.html', {'profile': profile})

@login_required
def create_or_edit_profile(request):
    userform = UserUpdateForm(instance=request.user)
    try:
        author = Author.objects.get(user=request.user)  # Get the Author object related to the logged-in user
    except Author.DoesNotExist:
        author = None  # If no Author exists, set to None

    authorform = ProfileUpdateForm(instance=author)
    mydict={'userform':userform,'authorform':authorform}
    author = Author.objects.get(user=request.user)  # Get the Author object related to the logged-in user

    if request.method == 'POST':
        userform = UserUpdateForm(request.POST, instance=request.user)
        if author:
            authorform = ProfileUpdateForm(request.POST, request.FILES, instance=author)
        else:
            authorform = ProfileUpdateForm(request.POST, request.FILES)
        if userform.is_valid() and authorform.is_valid():
            my_user=userform.save()
            # my_user.user = request.user
            # my_user.set_password(my_user.password)
            if 'password' in userform.changed_data:
                my_user.set_password(my_user.password)  # Set the password if it was changed
            my_user.save()

            #Saving the author profile elements
            author=authorform.save(commit=False)
            author.user=my_user  #author tied to current user
            author.save()
            messages.success(request, f"You successfully updated your profile")
        return redirect('users-profile')
    return render(request, 'users/edit_profile.html', context=mydict)
    
# def view_profile(request):
#     try:
#         profile = AuthorProfile.objects.get(user = request.user)
#     except AuthorProfile.DoesNotExist:
#         profile = None
    
#     return render(request, 'view_profile.html', {'profile':profile})
