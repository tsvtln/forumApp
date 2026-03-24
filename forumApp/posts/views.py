import asyncio
from datetime import datetime

import pytz
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.forms import modelform_factory
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import classonlymethod, method_decorator
from django.views import View
from django.views.generic import TemplateView, RedirectView, ListView, FormView, CreateView, UpdateView, DeleteView, \
    DetailView

from forumApp.decorators import measure_execution_time
from forumApp.posts.forms import PostBaseForm, PostCreateForm, PostDeleteForm, SearchForm, PostEditForm, CommentFormSet
from forumApp.posts.mixins import TimeRestrictedMixin
from forumApp.posts.models import Post


UserModel = get_user_model()


class BaseView:
    @classonlymethod
    def as_view(cls):

        def view(request, *args, **kwargs):
            view_instance = cls()
            return view_instance.dispatch(request, *args, **kwargs)

        return view

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.get(request, *args, **kwargs)

        elif request.method == 'POST':
            return self.post(request, *args, **kwargs)


@method_decorator(measure_execution_time, name="dispatch")
class IndexView(TimeRestrictedMixin, TemplateView):
    template_name = 'common/index.html'  # static

    extra_context = {
        'static_time': datetime.now(),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['dynamic_time'] = datetime.now()
        return context

    def get_template_names(self):  # dynamic
        if self.request.user.is_authenticated:
            return ['common/index_logged_in.html']
        else:
            return ['common/index.html']


# class Index(BaseView):
#     def get(self, request, *args, **kwargs):
#         # post_form = modelform_factory(
#         #     Post,
#         #     fields=('title', 'author', 'languages')
#         # )
#         #
#         # context = {
#         #     "my_form": post_form,
#         # }
#
#         context = {
#             'dynamic_time': datetime.now(),
#         }
#
#         return render(request, 'common/index.html', context)


# def index(request):
#     # form = PersonForm(request.POST or None)
#
#     ## DEBUG
#     # if request.method == "POST":
#     #     print(request.POST['person_name'])
#     #   if form.is_valid():
#     #       print(form.cleaned_data['person_name'])
#
#     post_form = modelform_factory(
#         Post,
#         fields=('title', 'author', 'languages')
#     )
#
#     context = {
#         "my_form": post_form,
#     }
#
#     return render(request, 'common/index.html', context)


# def dashboard(request):
#     form = SearchForm(request.GET)
#     posts = Post.objects.all()
#
#     if request.method == "GET":
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             posts = posts.filter(title__icontains=query)
#
#     context = {
#         "posts": posts,
#         "form": form,
#     }
#
#     return render(request, 'posts/dashboard.html', context)

class DashboardView(ListView, FormView):
    template_name = 'posts/dashboard.html'
    context_object_name = 'posts'
    form_class = SearchForm
    paginate_by = 6
    success_url = reverse_lazy('dash')

    model = Post

    def get_queryset(self):
        queryset = self.model.objects.all()
        print('DEBUG: All posts:', list(queryset))

        if 'posts.can_approve_posts' not in self.request.user.get_group_permissions() or not self.request.user.has_perm('posts.can_approve_posts'):
            queryset = queryset.filter(approved=True)
            print('DEBUG: Filtered approved posts:', list(queryset))

        if 'query' in self.request.GET:
            query = self.request.GET.get('query')
            queryset = queryset.filter(title__icontains=query)
            print('DEBUG: Filtered by query:', list(queryset))

        return queryset


async def fetch_post_and_users(post_id):
    post = await Post.objects.select_related('author').aget(pk=post_id)
    all_users = await sync_to_async(UserModel.objects.exclude)(id=post.author.id)
    all_users_to_list = await sync_to_async(list)(all_users)
    return post, all_users_to_list


async def send_slow_email(subject, message, origin, to):
    await asyncio.sleep(2)
    await sync_to_async(send_mail(
        subject,
        message,
        origin,
        [to]
    ))


async def notify_all_users(request, post_id):
    post, all_users = await fetch_post_and_users(post_id)
    subject = f"New post {post.title}"
    message = f"{post.author.username} wrote:\n\n{post.content}"
    email_tasks = [
        send_slow_email(
            subject,
            message,
            'no-reply@forumapp.com',
            user.email
        )
        for user in all_users
    ]

    await asyncio.gather(*email_tasks)

    return HttpResponse("DONE")


def approve_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.approved = True
    post.save()
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    # fallback to dashboard by URL name
    from django.urls import reverse
    return redirect(reverse('dash'))


# def add_post_view(request, pk):
#     post = Post.objects.get(pk=pk)
#     post.approved = True
#     post.save()


class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/add-post.html'
    success_url = reverse_lazy('dash')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# def add_post(request):
#     form = PostBaseForm(request.POST or None, request.FILES or None)
#
#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             return redirect('dash')
#
#     context = {
#         "form": form,
#     }
#
#     return render(request, 'posts/add-post.html', context)


class EditPostView(UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = 'posts/edit-post.html'
    success_url = reverse_lazy('dash')

    def get_form_class(self):
        if self.request.user.is_superuser:
            return modelform_factory(Post, fields=('title', 'content', 'author', 'languages'))
        else:
            return modelform_factory(Post, fields=('content',))


# def edit_post(request, pk: int):
#     post = Post.objects.get(pk=pk)
#
#     if request.method == 'POST':
#         form = PostEditForm(request.POST, instance=post)
#
#         if form.is_valid():
#             form.save()
#             return redirect('dash')
#
#     else:
#         form = PostEditForm(instance=post)
#
#     context = {
#         "form": form,
#         "post": post,
#     }
#
#     return render(request, 'posts/edit-post.html', context)

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/details-post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = CommentFormSet()
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        formset = CommentFormSet(request.POST or None)

        if request.method == 'POST':
            if formset.is_valid():
                for form in formset:
                    if form.cleaned_data:
                        comment = form.save(commit=False)
                        comment.post = post
                        comment.save()
                return redirect('details-post', pk=post.id)

        context = self.get_context_data()
        context['formset'] = formset

        return self.render_to_response(context)


#
# def details_page(request, pk: int):
#     post = Post.objects.get(pk=pk)
#     formset = CommentFormSet(request.POST or None)
#
#     if request.method == 'POST':
#         if formset.is_valid():
#             for form in formset:
#                 if form.cleaned_data:
#                     comment = form.save(commit=False)
#                     comment.post = post
#                     comment.save()
#             return redirect('details-post', pk=post.id)
#
#     context = {
#         "post": post,
#         "formset": formset,
#     }
#
#     return render(request, 'posts/details-post.html', context)

class DeletePostView(DeleteView):
    model = Post
    template_name = 'posts/delete-post.html'
    context_object_name = 'post'
    success_url = reverse_lazy('dash')


# def delete_post(request, pk: int):
#     post = Post.objects.get(pk=pk)
#     form = PostDeleteForm(instance=post)
#
#     if request.method == "POST":
#         post.delete()
#         return redirect('dash')
#
#     context = {
#         "form": form,
#         "post": post,
#     }
#
#     return render(request, 'posts/delete-post.html', context)


class RedirectHomeView(RedirectView):
    url = reverse_lazy('index')  # static way

    # dynamic way
    # def get_redirect_url(self, *args, **kwargs):
    #     pass
