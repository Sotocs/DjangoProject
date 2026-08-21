from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
    UpdateView,
    View,
)

from catalog.models import Product

from .forms import ProductForm


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all()
        return context


class ContactsView(TemplateView):
    template_name = "contacts.html"


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "product_detail.html"  # важно: полный путь с app-папкой
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context["product"]
        user = self.request.user

        # Проверка: может ли пользователь редактировать/удалять (владелец или суперпользователь)
        can_edit_or_delete = user.is_authenticated and (
            user.is_superuser or product.owner == user
        )

        # Проверка: может ли пользователь снимать с публикации (суперпользователь или имеет право)
        can_unpublish = user.is_authenticated and (
            user.is_superuser or user.has_perm("catalog.can_unpublish_product")
        )

        context.update(
            {
                "can_edit_or_delete": can_edit_or_delete,
                "can_unpublish": can_unpublish,
            }
        )
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_create.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"

    def get_success_url(self):
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # Разрешаем только владельцу или суперпользователю
        if not (request.user.is_superuser or obj.owner == request.user):
            from django.core.exceptions import PermissionDenied

            raise PermissionDenied("Вы не можете редактировать этот продукт")
        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:home")
    template_name = "product_confirm_delete.html"

    class ProductDeleteView(DeleteView):
        model = Product
        template_name = "catalog/product_confirm_delete.html"
        success_url = reverse_lazy("catalog:product_list")

        def dispatch(self, request, *args, **kwargs):
            obj = self.get_object()
            user = request.user

            can_delete = (
                user.is_superuser
                or obj.owner == user
                or user.has_perm(
                    "catalog.can_unpublish_product"
                )  # здесь используем то же кастомное право
            )

            if not can_delete:
                from django.core.exceptions import PermissionDenied

                raise PermissionDenied("У вас нет прав на удаление этого продукта")

            return super().dispatch(request, *args, **kwargs)


class UnpublishProductView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        # Проверка прав: суперпользователь ИЛИ право can_unpublish_product
        if not (
            request.user.is_superuser
            or request.user.has_perm("catalog.can_unpublish_product")
        ):
            messages.error(request, "У вас нет прав для снятия продукта с публикации.")
            # Важно: использовать catalog:product_detail из-за app_name
            return redirect("catalog:product_detail", pk=product.pk)

        # ИСПРАВЛЕНИЕ: меняем is_published, а не status
        product.is_published = False
        product.save()

        messages.success(request, "Продукт снят с публикации.")
        return redirect("catalog:product_detail", pk=product.pk)
