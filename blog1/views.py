from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.template.loader import get_template, render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic.base import View


from .models import post, Comments
# Create your views here.
from .forms import postForm, commentForm, SignUpForm

from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView

from .tokens import account_activation_token


class aboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = post
    def get_queryset(self):
        return post.objects.filter(published_date__lte= timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = post

    def has_permission(self):
        user = self.request.user
        return user.has_perm('post_edit') or user.has_perm('post_detail')

class PostCreateView(LoginRequiredMixin,CreateView):
    login_url = '/login/'

    form_class = postForm
    model = post
    success_url = reverse_lazy('post_list')

class PostUpdateView(LoginRequiredMixin,UpdateView,):
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

class SignUpView(View):
    form_class = SignUpForm
    template_name = 'registration/signup.html'


    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        user = form.save()
        user.save()
        html_file = get_template('registration/mail_template.html')
        html_content = html_file.render()
        msg = EmailMultiAlternatives(subject='test', from_email='shrbaral@gmail.com', to=['iamshrota@gmail.com'])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
        return render(request, 'blog1/index.html')



###################################
#@login_required
#def home(request): { using mail trap}
    #subject ='test'
    #message = ' You are logged in'
    #from_email = 'shrbaral@gmail.com'
    #recipient_list= ['iamshrota@gmail.com']
    #recipient_list = [request.user.email]
    #print(subject,message,from_email,recipient_list)
    #send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list)
    #return render(request,'blog1/index.html')
#################################
#@login_required
#def home(request): # here we have attached template
    #html_file = get_template('registration/mail_template.html')
    #html_content = html_file.render()
    #msg = EmailMultiAlternatives(subject='test',from_email='shrbaral@gmail.com',to=['iamshrota@gmail.com'])
    #msg.attach_alternative(html_content, 'text/html')
    #msg.send()
    #return render(request,'blog1/index.html')

###############################
def contact(request):
    if request.method=='POST':
        name = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        subject = request.POST.get('subject')

        sub= f"this msg is sent by {name} {lastname} from {country}"
        from_email = 'shrbaral@gmail.com'
        to = ['iamshrota@gmail.com']
        msg= subject
        send_mail(subject=sub,message=msg,from_email=from_email,recipient_list=to)
        return redirect('home')
    return render(request,'registration/contact.html')

############################
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