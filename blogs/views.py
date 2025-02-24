from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PostModel
from .forms import PostModelForm, SearchForm , CommentForm, ContactForm
from django.core.files.storage import default_storage
import tempfile
from django.shortcuts import get_object_or_404
import os
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    posts = PostModel.objects.all()
    # post_form = PostModelForm()
    comment_form = CommentForm()
    if request.method == 'POST' and 'post_form' in request.POST:
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

                # Handle the comment submission
    if request.method == 'POST' and  'comment_form' in request.POST:
        post_id = request.POST.get('post_id')  # Get the post_id where comment is being submitted
        post = PostModel.objects.get(id=post_id)  # Fetch the post object
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            # Create a comment object and associate it with the current post and user
            comment = comment_form.save(commit=False)
            comment.post = post
            # comment.user = request.user  # Assuming the user is logged in
            comment.save()
            messages.success(request, "Your comment has been posted.")
            return redirect('post-detail', post_id=post.id)  # Redirect to the post detail page

    else:
        comment_form = CommentForm()

    # comments = post.comments.all()  # Get all comments related to the current post
            
        context = {
        'posts' : posts,
        'form' : form,
        'comment_form': comment_form
        }

    return render(request, 'blog/index.html', context)

def post_detail(request, id):
    post = PostModel.objects.get(id=id)
    comments = post.comments.all()  # Get all comments related to this post
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            # comment.user = request.user
            comment.save()
            return redirect('post-detail', id=post.id)  # Reload the post with new comment
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'blog/post_detail.html', context)

def blog_post_list(request):
    form = SearchForm(request.GET)
    posts = PostModel.objects.all()

    if form.is_valid():
        query = form.cleaned_data['query']
        posts = posts.filter(title__icontains=query) | posts.filter(content__icontains=query)

    return render(request, 'blog/blog_post_list.html', {'form': form, 'posts': posts})


@login_required
def delete_blog_post(request, id):
     blog_post = get_object_or_404(PostModel, id=id)

     if blog_post.author != request.user:
            messages.error(request, message = "You are not authorized to delete this post because you're not the author.")
            return redirect('blog-index')  # Redirect to the blog list page if the user is not the author

     if request.method == 'POST':
        try:
            blog_post.delete()
            messages.success(request, message='You have successfully deleted the blog post!')
        except Exception as e:
            messages.error(request, message= 'Blog post not Deleted')
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
            
            # if 'image' in request.FILES:
            #     file_name = os.path.basename(request.FILES['image'].name)
            #     messages.success(request, message = f"Post updated successfully with {file_name} also added")
            # else:
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
            messages.success("Your issue has been Sent. We will get back to you shortly")
            return  redirect('blog-contact')
        else:
            messages.error("There was an error sending your issue. Please try again later")
    else:
        contact_form = ContactForm()
    instance = {
        'contact_form':contact_form
    }
    return render(request, 'blog/contact.html', instance)

# Post Detail View
# def post_detail(request, post_id):
#     post = Post.objects.get(id=post_id)
#     comments = post.comments.all()  # Fetch all comments related to the post

#     # Handling the form submission for new comments
#     if request.method == "POST":
#         author_name = request.POST['author_name']
#         content = request.POST['content']
#         comment = Comment(post=post, author_name=author_name, content=content)
#         comment.save()  # Save the new comment

#         # Redirect back to the same post detail page after submitting a comment
#         return HttpResponseRedirect(f"/post/{post_id}/")

#     return render(request, 'post_detail.html', {'post': post, 'comments': comments})