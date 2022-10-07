from django.shortcuts import get_object_or_404, render

from .forms import EmailPostForm
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail



# Create your views here.
def post_list(request):
    all_posts = Post.published.all()

    paginator = Paginator(all_posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.xhtml', {
        'posts': posts,
    })


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day
                             )
    return render(request, 'blog/post/detail.xhtml', {
        'post': post,
    })


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends that you read '{post.title}'"
            message = f"Read {post.title} at {post_url}\n\n"\
                      f"{cd['name']} wrote the following comment about the post:\n {cd['comments']}"
            send_mail(subject, message, 'tbbotchwey01@gmail.com', [cd['to']])
            
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.xhtml', {
        'post': post,
        'form': form,
        'sent': sent,
    })            
class PostListView(ListView):
    queryset: Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.xhtml'