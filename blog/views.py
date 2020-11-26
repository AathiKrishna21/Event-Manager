from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Post
from .forms import PostRegisterForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import csv
@login_required
def home(request):
    context = {
        'posts' : Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted'] 
    paginate_by = 5


class UserPostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content','image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

@login_required
def register(request, pk):
    if request.method == "POST":
        obj=Post.objects.get(id=pk)
        form = PostRegisterForm(request.POST)
        if form.is_valid():
            t=[]
            name = form.cleaned_data.get('name')
            t.append(name)
            regno = form.cleaned_data.get('regno')
            t.append(regno)
            email =form.cleaned_data.get('email')
            t.append(email)
            phone =form.cleaned_data.get('phone')
            t.append(phone)
            dept = form.cleaned_data.get('dept')
            t.append(dept)
            event=obj.title
            t.append(event)
            f_name=obj.register_file.path
            with open(f_name, 'a',newline='') as f:
                writer=csv.writer(f)
                writer.writerow(t)
            return redirect("blog-home")

        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

            return render(request = request,
                          template_name = "blog/pregister.html",
                          context={"form":form})

    form = PostRegisterForm
    return render(request = request,
                  template_name = "blog/pregister.html",
                  context={"form":form}) 
@login_required
def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})