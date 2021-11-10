from django import http
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.http import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required,permission_required
from django.utils.decorators import method_decorator
# Create your views here.

from django.views import generic
from django.views.generic.edit import CreateView,UpdateView,DeleteView, ModelFormMixin
from .models import Article,Comment,Category



# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


class ArticleList(generic.ListView):
    queryset = Article.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    context_object_name= 'Article_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
class UnpublishedPosts(generic.ListView):
    queryset = Article.objects.filter(status=0).order_by('-created_on')
    template_name = 'index.html'
    context_object_name= 'Article_list'
    
    @method_decorator(login_required)
    @method_decorator(permission_required('blogApp.update_article'))
    def dispatch(self, *args, **kwargs):
        return super(UnpublishedPosts, self).dispatch(*args, **kwargs)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        
        return context

class ArticleDetail(generic.DetailView):
    model = Article
    template_name = 'Article_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        articleIdentifier = Article.objects.get(slug=self.kwargs['slug'])
        context['comments'] = Comment.objects.filter(article = articleIdentifier)
        return context
    
    
class ArticleCreate(CreateView):
    model = Article
    fields = ['title','category','content','picture',]
    template_name = 'article_form.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ArticleCreate, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
    
    def form_valid(self,form):
        try : 
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            self.object.save()
            return super(ModelFormMixin, self).form_valid(form)
        
        except(ValueError):
            return(HttpResponseRedirect("../../accounts/login"))
    
class ArticleDelete(DeleteView):
    model = Article
    success_url ="/"
    
    @method_decorator(login_required)
    @method_decorator(permission_required('blogApp.delete_article'))
    def dispatch(self, *args, **kwargs):
        print (self.request.user.has_perm('blogApp.delete_article'))
        return super(ArticleDelete, self).dispatch(*args, **kwargs)
    
class ArticleUpdateView(UpdateView):
    model = Article
    fields = ['title','category','content','picture']
    template_name = '_update_form'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        
        """ Making sure that only authors can update articles """
       
        obj = self.get_object()
        if obj.author != self.request.user:
            return login_view(request)
        return super(ArticleUpdateView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
    
class ArticleCommentView(CreateView):
    model = Comment
    fields = ['content']
    context_object_name = 'context'
    template_name = 'comment_form.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ArticleCommentView, self).dispatch(*args, **kwargs)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
    
    def form_valid(self,form):
        try : 
            self.object = form.save(commit=False)
            slugIdentifier = self.kwargs['slug']
            self.object.article = Article.objects.get(slug=slugIdentifier)
            self.object.commenter = self.request.user
            self.object.save()
            return super(ModelFormMixin, self).form_valid(form)
        except(ValueError):
            return(HttpResponseRedirect("../../accounts/login"))
        
class CommentDetail(generic.ListView):
    template_name = 'comment_detail.html'
    context_object_name = 'object'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
    
    def get_queryset(self):
        articleIdentifier = Article.objects.get(slug=self.kwargs['slug'])
        queryset = Comment.objects.filter(article = articleIdentifier)
        return queryset
        
        
class CommentDelete(DeleteView):
    model = Comment
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.success_url = self.request.META.get('HTTP_REFERER')
        return super(CommentDelete, self).dispatch(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
    
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url ="/blog/"
    template_name = 'registration/signup.html'
    
    
class categoryView(generic.ListView):
    template_name = 'index.html'
    context_object_name= 'Article_list'
    success_url ="/"
    
    def get_queryset(self):
        Categorydentifier = Category.objects.get(id = self.kwargs['pk'])
        queryset = Article.objects.filter(status=1,category  = Categorydentifier)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
@login_required
def PublishArticle(request, identifier):
    post = Article.objects.get(slug = identifier)
    post.status = 1
    post.save()
    return redirect('blogApp:article_list')
    
