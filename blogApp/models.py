from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    
    def __str__(self):
        return self.name
    
#statuses of blog posts stored in a tuple
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField()
    status = models.IntegerField(choices=STATUS, default=0)


    class Meta:
        ordering = ['-created_on']
        
    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
    
        
    def get_absolute_url(self):
        return reverse('blogApp:article_details', kwargs = {'slug':self.slug})
    
        
    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete= CASCADE)
    commenter = models.ForeignKey(User, on_delete= models.CASCADE,related_name='comment_posts')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True, null = True)
    
    def __str__(self):
        return self.content
    
    def get_absolute_url(self):
        return reverse('blogApp:article_details', kwargs = {'slug':self.article.slug})
    
    