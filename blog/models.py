from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.shortcuts import redirect
from django.db.models import Q
from django.urls import reverse

# Create your models here.
class Author(models.Model):
    name = models.OneToOneField(User, unique=True, max_length=64, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    phone_no = models.IntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(max_length=1000, blank=True, null=True)
    photo = models.ImageField(upload_to='author_img/', blank=True, null=True)
    joined_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=264, unique=True, null=True, blank=True)
    about = models.TextField(max_length=5000, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        unique_together = ('name', 'slug')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:author',kwargs={'slug':self.slug})

def slg_gen(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug =instance.name

pre_save.connect(slg_gen, sender=Author)

class Post(models.Model):
    STATUS = (
            ('D','draft'),
            ('P','published')
         )
    PRIVACY = (
        ('Public','Public'),
        ('Private','Private')
    )
    title = models.CharField(max_length=100)
    creator = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField(max_length=10000 ,blank=True, null=True)
    post_pic = models.ImageField(upload_to='post_img/' , null=True, blank=True)
    slug = models.SlugField(max_length=100, unique='True', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(choices=STATUS, max_length=2, default='D')
    privacy = models.CharField(choices=PRIVACY, max_length=8, default='Public')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-published_date',)
        unique_together = ('title', 'slug')

    def get_absolute_url(self):
        return reverse('blog:posts')

def slug_gen(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug ='-'.join(instance.title.split())

pre_save.connect(slug_gen, sender=Post)

class Public_Posts_Manager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(~Q(status='D'), ~Q(privacy='Private'))

class Public_Post(Post):
    objects = Public_Posts_Manager()
    class Meta:
        proxy = True

class Author_Posts_Manager(models.Manager):
    def get_queryset(self):
        # return super().get_queryset().filter(status='P', privacy='Public')
        return super().get_queryset().all()

class Author_Post(Post):
    objects = Author_Posts_Manager()
    class Meta:
        proxy = True

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    body = models.TextField(max_length=1500)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_date',)

    def __str__(self):
        return f" {self.name} commented on {self.created_date}"

class ContactUs(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    subject = models.CharField(max_length=264, blank=False, null=False)
    body = models.TextField(max_length=2000, blank=False, null=False)