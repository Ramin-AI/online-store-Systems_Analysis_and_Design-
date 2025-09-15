from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    """
    Form for creating and editing products.
    """
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'inventory', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ProductFilterForm(forms.Form):
    """
    Form for filtering products by category.
    """
    category = forms.ChoiceField(required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Use the predefined category choices from the Product model with icons
        category_icons = {
            '': '<i class="fas fa-th-large"></i> All Categories',
            'Laptop': '<i class="fas fa-laptop"></i> Laptop',
            'Graphics Card': '<i class="fas fa-microchip"></i> Graphics Card',
            'Game Console': '<i class="fas fa-gamepad"></i> Game Console',
            'Monitor': '<i class="fas fa-desktop"></i> Monitor',
            'Mobile': '<i class="fas fa-mobile-alt"></i> Mobile'
        }
        
        # Create choices with icons
        category_choices = [(key, category_icons[key]) for key in [''] + [choice[0] for choice in Product.CATEGORY_CHOICES]]
        self.fields['category'].choices = category_choices