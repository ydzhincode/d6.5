from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView
from .models import Post, Category, PostCategory, Author
from django.shortcuts import render, redirect
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import os
from pathlib import Path
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta


class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 10
    form_class = PostForm

class NewsDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'
# Create your views here.


class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'

    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
            context = super().get_context_data(**kwargs)
            context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст

            context['categories'] = Category.objects.all()
            context['form'] = PostForm()
            return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST) # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid(): # если пользователь ввёл всё правильно и нигде не накосячил, то сохраняем новый товар
            form.save()
            return super().get(request, *args, **kwargs)

class PostDetailView(DetailView):
    template_name = 'news_detail.html'
    model = Post
    context_object_name = 'new'

class PostCreateView(PermissionRequiredMixin, CreateView):

    template_name = 'news_create.html'
    form_class = PostForm
    permission_required = ('news.add_post')
    #success_url = reverse_lazy('news_list')
    def form_valid(self, form):

        super().form_valid(form)

        #today = timezone.localdate()

        author = Author.objects.get(authorUser_id=self.request.user.id)
        yesterday = datetime.now() - timedelta(days=1)
        post_day = Post.objects.filter(author=author, dateCreation__gt=yesterday).count()
        #post_day = Post.objects.filter(author=self.request.user, dateCreation__date=today).count()
        print(post_day)
        if post_day > 3:
            last_post = Post.objects.filter(author=author, dateCreation__gt=yesterday).order_by('-dateCreation').last()
            print(last_post)
            if last_post:
                last_post.delete()

            raise ValidationError("Вы достигли лимита на создание новостей за день.")
            return redirect('403_error.html/')





# дженерик для редактирования объекта
class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'news_create.html'
    form_class = PostForm
    permission_required = ('news.change_post')
# метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)



# дженерик для удаления товара
class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('news_list')
    permission_required = 'news.delete_post'


class CategoryView(DetailView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context['category'] = Category.objects.get(pk=self.kwargs['pk'])
        context['subscribers'] = category.subscribers.all()
        return context

@login_required
def subscribe_from_category(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribers.add(request.user.id)

    html_content = render_to_string(
        'subscribe.html',
        {
            'category': category,
            'user': request.user,

        }
    )
    msg = EmailMultiAlternatives(
        subject= {category},
        body = '',
        from_email = 'managernewssk@mail.ru',
        to = ['elkarimova@gmail.com'],
        )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    try:
        msg.send()
    except Exception as e:
        print(f"Error sending email: {e}")


    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe_from_category(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribers.remove(request.user.id)
    return redirect(request.META.get('HTTP_REFERER'))











