from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy, reverse

from .forms import PostForm
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"
    paginate_by = 5

    # ФИЛЬТРАЦИЯ ОПУБЛИКОВАННЫХ СТАТЕЙ
    def get_queryset(self):
        # Возвращаем только опубликованные записи
        return Post.objects.filter(is_published=True)


class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"

    # УВЕЛИЧЕНИЕ СЧЁТЧИКА ПРОСМОТРОВ
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views += 1
        obj.save(update_fields=["views"])
        return obj


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "post_form.html"
    success_url = reverse_lazy("blog:post_list")


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "post_form.html"

    # ПЕРЕНАПРАВЛЕНИЕ ПОСЛЕ РЕДАКТИРОВАНИЯ НА ПРОСМОТР ЭТОЙ СТАТЬИ
    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.pk})


class PostDeleteView(DeleteView):
    model = Post
    template_name = "post_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")
