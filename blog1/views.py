from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone

from .models import post, Comments
# Create your views here.
from .forms import postForm, commentForm

from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView


class aboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = post
    def get_queryset(self):
        return post.objects.filter(published_date__lte= timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = post

class PostCreateView(LoginRequiredMixin,CreateView):
    login_url = '/login/'

    form_class = postForm
    model = post
    success_url = reverse_lazy('post_list')

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    success_url = reverse_lazy('post_list')
    form_class = postForm
    model = post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = post
    success_url = reverse_lazy('post_list')

class PostDraftView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog1/post_list.html'
    model = post

    def get_queryset(self):
        return post.objects.filter(published_date__isnull=True).order_by('created_date')

###################################
@login_required
def post_publish(request,pk ):
    Post = get_object_or_404(post, pk=pk)
    Post.publish
    return redirect('post_detail', pk=pk)



@login_required
def add_comment_to_post(request,pk):
    Post = get_object_or_404(post, pk=pk)
    if request.method == "POST":
        form = commentForm(request.POST)
        if form.is_valid():
            Comments = form.save(commit=False)
            Comments.Post = post
            Comments.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = commentForm()
    return render(request, 'blog1/comment_form.html', {'form': form})
@login_required
def comment_approve(request,pk ):
    comment = get_object_or_404(Comments,pk=pk)
    comment.approve()
    return redirect('post_detail', pk= comment.post.pk)

@login_required
def comment_remove(request,pk ):
    comment = get_object_or_404(Comments,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)

from django.conf import settings
User = settings.AUTH_USER_MODEL