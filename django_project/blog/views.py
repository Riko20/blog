from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import View
from .forms import TagForm, PostForm, UserForm
from .models import Post, Tag
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.models import User

## check check

def searching(request):
    posts = Post.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query)|Q(body__icontains=search_query))
    return posts

def pagination(request, query_for_pagin, quantity):
    paginator = Paginator(query_for_pagin, quantity)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginating = page.has_other_pages()

    if page.has_previous():
        prev_page = '?page={}'.format(page.previous_page_number())
    else:
        prev_page = ''

    if page.has_next():
        next_page = '?page={}'.format(page.next_page_number())
    else:
        next_page = ''

    context = {'page_obj': page, 'is_pag': is_paginating, 'prev_page': prev_page, 'next_page': next_page}
    return context

class PostList(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>(list tyt).html
    context_object_name = 'posts'
    ordering = ['-date_pub']
    paginate_by = 2

# def home(request):    !!changed!!
#     posts = searching(request)
#     context = pagination(request, posts, 5)
#     return render(request, 'blog/home.html', context)



class PostDetail(DetailView):
    model = Post
    template_name = 'blog/about.html'
    context_object_name = 'post'


class MixinDetail:
    model = None
    templ = None

    def get(self, request, slug):
        context_value = get_object_or_404(self.model, slug__iexact=slug)
        return render(request, self.templ, context={'{}'.format(self.model.__name__.lower()): context_value, 'admin_panel': context_value, 'obj': True})

class CreateMixin:
    form = None
    template = None

    def get(self, request):
        form = self.form
        return render(request, self.template, context={'form': form})

    def post(self, request):
        bound_form = self.form(request.POST)

        if bound_form.is_valid():
            new_model = bound_form.save()
            return redirect(new_model)

        return render(request, self.template, context={'form': bound_form})


class ObjectUpdate:
    object_form = None
    object_model = None
    template = None

    def get(self, request, slug):
        obj = self.object_model.objects.get(slug__iexact=slug)
        form = self.object_form(instance=obj)
        return render(request, self.template, context={'form': form, 'obj': obj})

    def post(self, request, slug):
        obj = self.object_model.objects.get(slug__iexact=slug)
        bound_form = self.object_form(request.POST, instance=obj)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)

        return render(request, self.template, context={'form': bound_form, 'obj': obj})

class ObjectDelete:
    object_model = None
    template = None
    to_reverse = None

    def get(self, request, slug):
        obj = self.object_model.objects.get(slug__iexact=slug)
        return render(request, self.template, context={'{}'.format(self.object_model.__name__.lower()): obj})

    def post(self, request, slug):
        obj = self.object_model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse('blog-home'))

#  1 method
# class PostCreate(LoginRequiredMixin, CreateMixin, View):
#     form = PostForm
#     templates = 'blog/post_create.html'
#     raise_exception = True


# 2 method
class PostCreate(CreateView):
    model = Post
    fields = ['title', 'body']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, ObjectUpdate, View):
    object_model = Post
    object_form = PostForm
    template = 'blog/post_update.html'
    raise_exception = True

# 2 method

class PostUpdate(UpdateView):
    model = Post
    fields = ['title', 'body']




# class PostDetail(MixinDetail, View):
#     model = Post
#     templ = 'blog/about.html'

class PostDelete(LoginRequiredMixin ,ObjectDelete, View):
    object_model = Post
    template = 'blog/post_delete.html'
    to_reverse = 'blog-home'
    raise_exception = True





def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags.html', context={'tags': tags})




class TagUpdate(LoginRequiredMixin ,ObjectUpdate, View):
    object_form = TagForm
    object_model = Tag
    template = 'blog/tag_update.html'
    raise_exception = True




class TagCreate(LoginRequiredMixin ,View):

    def get(self, request):
        form = TagForm()
        context_val = {'form': form}
        return render(request, 'blog/tag_create.html', context_val)

    def post(self, request):
        form_inst = TagForm(request.POST)

        if form_inst.is_valid():
            new_t = form_inst.save()
            return redirect(new_t)

        return render(request, 'blog/tag_create.html', context={'form': form_inst})

    raise_exception = True


class TagDelete(LoginRequiredMixin ,ObjectDelete, View):
    object_model = Tag
    template = 'blog/tag_delete_url.html'
    to_reverse = 'tag_list_url'
    raise_exception = True




class TagDetail(MixinDetail, View):
    model = Tag
    templ = 'blog/tag_detail.html'

#  Old method, new one with function and UserCreationForm
class CreateUser(View):

    def get(self, request):
        user_form = UserForm()
        return render(request, 'blog/registrate.html', context={'user_form': user_form})

    def post(self, request):
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data.get('username')
            messages.success(request, 'Account is created for: {}'.format(username))
            return redirect('blog-home')

        return render(request, 'blog/registrate.html', context={'user_form': user_form})





