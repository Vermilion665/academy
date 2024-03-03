from django.urls import path

from products.views import *


app_name = 'products'

urlpatterns = [
    path('', index, name='index'),
    path('products-form/', ProductCreateView.as_view(), name='products-form'),
    path('lesson-form/', LessonCreateView.as_view(), name='lesson-form'),
    path('products-detail/<slug:slug>', ProductDetailView.as_view(), name='products-detail'),
    path('lesson-list/', LessonListView.as_view(), name='lesson-list'),
]