from django.db import models

# Create your models here.
class Bookitem(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, default=1)
    
    class Meta:
        indexes = [
            models.Index(fields=['price']),
        ]

class Category(models.Model): 
    slug = models.SlugField()
    title = models.CharField(max_length=255)
    
    def __str__(self)-> str:
        return self.title