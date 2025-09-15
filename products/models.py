from django.db import models
from django.urls import reverse
import os

class Product(models.Model):
    """
    Product model as specified in the UML class diagram.
    """
    # Category choices as specified in the requirements
    LAPTOP = 'Laptop'
    GRAPHICS_CARD = 'Graphics Card'
    GAME_CONSOLE = 'Game Console'
    MONITOR = 'Monitor'
    MOBILE = 'Mobile'
    
    CATEGORY_CHOICES = [
        (LAPTOP, 'Laptop'),
        (GRAPHICS_CARD, 'Graphics Card'),
        (GAME_CONSOLE, 'Game Console'),
        (MONITOR, 'Monitor'),
        (MOBILE, 'Mobile'),
    ]
    
    # Map categories to folder names
    CATEGORY_FOLDERS = {
        LAPTOP: 'laptops',
        GRAPHICS_CARD: 'Graphics card',
        GAME_CONSOLE: 'Game console',
        MONITOR: 'Monitor',
        MOBILE: 'Mobile',
    }
    
    def category_image_path(instance, filename):
        """Generate the path for the image based on the product category"""
        category_folder = Product.CATEGORY_FOLDERS.get(instance.category, 'products')
        return os.path.join('product pictures', category_folder, filename)
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    inventory = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to=category_image_path, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])
    
    def get_details(self):
        """
        Return product details as a string.
        """
        return f"{self.name} - {self.description} - ${self.price}"
    
    def update_stock(self, quantity):
        """
        Update the inventory stock of the product.
        """
        self.inventory += quantity
        self.save()
        return self.inventory
        
    def is_available(self):
        """
        Check if the product is available (has inventory > 0).
        """
        return self.inventory > 0