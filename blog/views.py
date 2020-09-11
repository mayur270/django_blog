from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Post, Author, Contact
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .forms import CommentForm, PostForm, ContactForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def blog_home(request):
    all_posts = Post.objects.filter(featured=True).order_by('-timestamp')
    paginator = Paginator(all_posts, 12)
    page_request = 'page'
    page = request.GET.get(page_request)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    context={
        'all_posts':paginated_queryset,
        'page_request': page_request,
        }
    return render(request, 'blog/home.html', context)

def blog_about(request):
    return render(request, 'blog/about.html')

def blog_contact(request):
    form=ContactForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect(reverse('contact_confirmation'))
    context = {
        'form':form,
    }
    return render(request, 'blog/contact.html', context)

def contact_confirmation(request):
    return render(request, 'blog/contact_confirmation.html')

def blog_search(request):
    all_posts = Post.objects.all()
    query = request.GET.get('q')
    if query:
        all_posts = all_posts.filter(
            Q(title__icontains=query)
        ).distinct()
    context = {
        'all_posts':all_posts,
    }
    return render(request, 'blog/search.html', context)

def blog_single(request, id):
    blog_detail_post = get_object_or_404(Post, id=id)
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post_id = blog_detail_post.id
            form.save()
            return redirect(reverse('blog_single', kwargs={
                'id': blog_detail_post.id
            }))
    context = {
        'blog_detail_post':blog_detail_post,
        'form':form
    }
    return render(request, 'blog/blog-single.html', context)

def get_author(user):
    qs = Author.objects.filter(user=user)
    if not qs.exists():
        Author.objects.get_or_create(user=user)
        qs = Author.objects.filter(user=user)
        return qs[0]
    return qs[0]

@login_required
def blog_create(request):
    title ='Add'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('blog_single', kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form':form
    }
    return render(request, 'blog/blog-create.html', context)

@login_required
def blog_update(request, id):
    title='Update'
    blog_update_post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=blog_update_post)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            if form.instance.author == author:
                form.save()
                return redirect(reverse('blog_single', kwargs={
                    'id': form.instance.id
                }))
    context = {
        'title': title,
        'form':form
    }
    return render(request, 'blog/blog-create.html', context)

@login_required
def blog_delete(request, id):
    blog_delete_post = get_object_or_404(Post, id=id)
    blog_delete_post.delete()
    return redirect(reverse("blog_home"))
