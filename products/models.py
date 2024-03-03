from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from slugify import slugify

# Сущность продукта
class Product(models.Model):
    author = models.CharField(max_length=100, verbose_name='Автор')
    name = models.CharField(max_length=100, verbose_name='Название курса', unique=True)
    start_date = models.DateTimeField(verbose_name='Старт курса')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    min_users_per_group = models.IntegerField(default=3)
    max_users_per_group = models.IntegerField(default=6)
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL-имя', editable=False)

    
    @property
    def num_lessons(self):
        return Lesson.objects.filter(product=self)

    def get_absolute_url(self):
        return reverse('products:products-detail', kwargs={
            'slug': self.slug
            }
        )
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
    

# Сущность описывающая доступ к продукту у аутентифицированного пользователя
class UserAccess(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


# Сущность урока
class Lesson(models.Model):
    product =models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name='Название урока', unique=True)
    video_link = models.URLField(verbose_name='Ссылка на видео')


# Сущность группы
class Group(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Название группы')
    students = models.ManyToManyField(User)

    def get_users_access(self):
        """Получение списка пользователей имеющих доступ к продукту"""
        return [user_access.user for user_access in UserAccess.objects.filter(product=self.product, access=True)]
    
    def distribute_users_to_groups(self):
        """Алгоритм распределения пользователей, которые имеют доступ, по группам"""
        if not self.product.start_date > timezone.now():
            return
        
        users = self.get_users_access()
        total_users = len(users)
        max_users = self.product.max_users_per_group
        min_users = self.product.min_users_per_group
        num_groups = (total_users + max_users - 1) // max_users
        groups = [[] for _ in range(num_groups)]

        # Распределение по группам с учётом минимального и максимального значений
        i = 0
        for user in users:
            if len(groups[i]) < min_users:
                groups[i].append(user)
            i = (i + 1) % num_groups

        for j in range(num_groups):
            self.students.add(*groups[j])
    