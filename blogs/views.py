from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PostModel,Comment,Contacts
from .forms import PostModelForm, SearchForm , CommentForm, ContactForm
from django.core.files.storage import default_storage
import tempfile
from django.shortcuts import get_object_or_404
import os
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator




# Create your views here.


def index(request):
    posts = PostModel.objects.all()
    if request.method == 'POST':
        form =  PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            if request.user.is_authenticated:
                instance.author = request.user
            else:
                request.session['form_data'] = request.POST
                return redirect('users-login')
            instance.save()
            messages.success(request, "You successfully posted on Blogspot.")
            return redirect('blog-index')
    else:
        # Check if there's saved form data in the session
        form_data = request.session.pop('form_data', None)
        if form_data:
            form = PostModelForm(form_data)  # Pre-populate the form with saved data
        else:
            form = PostModelForm()
        
        paginator = Paginator(posts, 2)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
        'posts' : posts,
        'form' : form,
        'page_obj': page_obj,
        }

    return render(request, 'blog/index.html', context)

def post_detail(request, id):
    post = PostModel.objects.get(pk=id)
    comments = post.comment_set.all()  # Get all comments related to this post
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blog = post
            # comment.user = request.user
            comment.save()
            messages.success(request, "Your comment has been posted.")
            return redirect('post-detail', id=id)  # Reload the post with the new comment
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'blog/post_detail.html', context)

@login_required(login_url="users-login")    
def delete_comment(request, id, comment_id):
     blog = get_object_or_404(PostModel, pk = id)
     comment = get_object_or_404(Comment, pk = comment_id, blog = blog)
     if blog.author != request.user or not request.user.is_staff:
            messages.error(request, message = "You are not authorized to delete this comment because you're not the post author.")
            return redirect('post-detail', id = id)  # Redirect to the blog list page if the user is not the author

     if request.method == 'POST':
        try:
            comment.delete()
            messages.error(request, message='You have successfully deleted the comment!')
        except Exception as e:
            messages.error(request, message= 'Comment not Deleted')
        return redirect('post-detail', id = id)
     else:
        # Show a confirmation page before deletion
        return render(request, 'blog/confirm_comment_delete.html', {'comment': comment})

@login_required(login_url="users-login")    
def admin_delete_feedback(request, feedback_id):
    # blog = get_object_or_404(PostModel, id=id)
    feedback = get_object_or_404(Contacts, pk=feedback_id)

    if not request.user.is_staff:
        messages.error(request, message="You are not authorised to delete ths comment!!")
        return redirect("blog-feedbacks")
    try:
        feedback.delete()
        messages.error(request, message="You have successfully deleted the feedback")
    except Exception as e:
        messages.error(request, message="Feedback not deleted!")
    return redirect("blog-feedbacks")


@login_required(login_url="users-login")    
def approve_feedback(request, feedback_id):
    feedback = get_object_or_404(Contacts, pk=feedback_id)

    if not request.user.is_staff:
        messages.error(request, message="You are not authoriseed to perform this operation!")
        return redirect("blog-feedbacks")
    
    feedback.approved = True
    feedback.save()
    messages.success(request, message=f"You have successfully approved the feedback from {feedback.your_name}")
    return redirect("blog-feedbacks")


@login_required
def delete_blog_post(request, id):
     blog_post = get_object_or_404(PostModel, id=id)

     if blog_post.author != request.user:
            messages.error(request, message = "You are not authorized to delete this post because you're not the author.")
            return redirect('blog-index')  # Redirect to the blog list page if the user is not the author

     if request.method == 'POST':
        try:
            blog_post.delete()
            messages.error(request, message='You have successfully deleted the post!')
        except Exception as e:
            messages.error(request, message= 'The post Could not be Deleted!')
        return redirect('blog-index')
     else:
        # Show a confirmation page before deletion (optional)
        return render(request, 'blog/confirm_delete.html', {'post': blog_post})

@login_required
def update_blog_post(request, id):
    blog_post = get_object_or_404(PostModel, id=id)
    
    # If the request method is POST, handle form submission
    if request.method == 'POST':
        form = PostModelForm(request.POST, request.FILES, instance=blog_post) # Bind the form with the current blog post
        if form.is_valid():
            form.save() # Save the updated data to the database
            messages.success(request, message = "You successfully updated your post")
            return redirect('blog-index')
        else:
            messages.error(request, "There was an error updating your post")

    # If the request method is GET, just display the current data in the form
    else:
        form = PostModelForm(instance=blog_post)
    return render(request, 'blog/update_blog.html', {'form': form, 'post':'blog_post'})


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    contact_form =  ContactForm()
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, message="Your issue has been received. We will get back to you shortly")
            return  redirect('blog-contact')
        else:
            messages.error("There was an error sending your issue. Please try again later")
    else:
        contact_form = ContactForm()
    instance = {
        'contact_form':contact_form,
    }
    return render(request, 'blog/contact.html', instance)


def feedbacks(request):
    feedbacks = Contacts.objects.all()
    feedbacks = feedbacks

    instance = {
        'feedbacks': feedbacks,
    }

    return render(request, 'blog/feedbacks.html', instance )

def search_view(request):
    query = request.GET.get('query', '')
    form = PostModelForm()
    posts = PostModel.objects.all()

    if query:
        posts = posts.filter(title__icontains=query) | posts.filter(author__username__icontains=query)
        post_number = posts.count()
    paginator = Paginator(posts, 3)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    word = f"Search Results: {post_number} {'post' if post_number == 1 else '' if post_number == 0 else 'posts'}"



    context = {
        'form' : form,
        'word': word,
        'page_obj' : page_obj,
        'post_number': post_number,
    }

    return render(request, 'blog/search_results.html', context)