from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, ListView

from .models import Product, Lesson

def index(request):
    list = Product.objects.all()
    return render(request, 'products/index.html', {'list': list})


class ProductCreateView(CreateView):
    model = Product
    fields = '__all__'
    template_name = 'products/products-form.html'
    success_url = reverse_lazy('products:index')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/products-detail.html'
    context_object_name = 'products'
    slug_url_kwarg = 'slug'


class LessonCreateView(CreateView):
    model = Lesson
    fields = '__all__'
    template_name = 'products/lesson-form.html'
    success_url = reverse_lazy('products:lesson-list')


class LessonListView(ListView):
    model = Lesson
    fields = '__all__'
    template_name = 'products/lesson-list.html'
    context_object_name = 'lessons'
