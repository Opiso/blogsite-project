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
from blogs.models import PostModel
from django.utils import timezone
from django.db.models import Q
from django.db.models import Count
from datetime import date







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

@login_required(login_url="users-login")    
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

@login_required(login_url="users-login")    
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
    
@login_required(login_url="users-login")    
def admin_dashboard(request):

    # Get the total count of posts and users
    total_posts = PostModel.objects.count()
    total_users = User.objects.count()

    # Get the user with the most posts and the number of posts for him/her
    most_active_user = User.objects.annotate(num_posts=Count('postmodel')).order_by('-num_posts').first()
    most_active_user_posts = most_active_user.num_posts if most_active_user else 'No posts yet'

    # Get the name of the user with the highest number of posts
    most_active_user_name = most_active_user.username if most_active_user else 'No posts yet'

    # Get the current time, adjusted to the local timezone
    time_now = timezone.localtime(timezone.now())

    # set the filtering bases
    start_of_year = date(time_now.year,1, 1)
    start_of_month = date(time_now.year, time_now.month, 1)
    start_of_day = date(time_now.year, time_now.month, time_now.day)

    # Get posts for the current year
    posts_this_year = PostModel.objects.filter(
        date_created__gte=start_of_year,
        date_created__lte=time_now
    ).count()
    # Get posts created this month
    posts_this_month = PostModel.objects.filter(
        date_created__gte=start_of_month,
        date_created__lte=time_now
    ).count()

    # Get posts created today
    posts_today = PostModel.objects.filter(
        date_created__gte=start_of_day,
        date_created__lte=time_now
    ).count()

    context = {
        'total_posts': total_posts,
        'total_users': total_users,
        'posts_this_year': posts_this_year,
        'posts_this_month': posts_this_month,
        'posts_today': posts_today,
        'month': time_now.strftime('%B'),  # Month as a string (e.g., March)
        'year': time_now.year,
        'month2': time_now.month,  # Month as an integer (e.g., 3 for March)
        'day': time_now.date(),
        'time': time_now,
        'most_active_user_name': most_active_user_name,
        'most_active_user_posts': most_active_user_posts,
    }

    return render(request, 'users/admin_dashboard.html', context)

@login_required(login_url="users-login")
def view_users(request):
    # Get all users
    users = User.objects.all()
    
    return render(request, 'users/registered_customers.html', {'users':users})
