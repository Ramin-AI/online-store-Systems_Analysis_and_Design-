from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Product
from .forms import ProductForm, ProductFilterForm

def product_list(request):
    """
    Display a list of all available products with optional filtering.
    """
    products = Product.objects.all()
    
    # Handle category filtering
    form = ProductFilterForm(request.GET)
    if form.is_valid() and form.cleaned_data['category']:
        products = products.filter(category=form.cleaned_data['category'])
    
    context = {
        'products': products,
        'filter_form': form,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    """
    Display detailed information for a single product.
    """
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)

# Admin functions
def is_admin(user):
    """
    Check if the user is an admin (staff).
    """
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_product_list(request):
    """
    Display a list of all products for admin management.
    """
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'products/admin_product_list.html', context)

@login_required
@user_passes_test(is_admin)
def add_product(request):
    """
    Add a new product to the store catalog.
    """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('admin_product_list')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'title': 'Add Product',
    }
    return render(request, 'products/product_form.html', context)

@login_required
@user_passes_test(is_admin)
def edit_product(request, pk):
    """
    Edit an existing product.
    """
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('admin_product_list')
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'title': 'Edit Product',
        'product': product,
    }
    return render(request, 'products/product_form.html', context)

@login_required
@user_passes_test(is_admin)
def delete_product(request, pk):
    """
    Delete a product from the store catalog.
    """
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('admin_product_list')
    
    context = {
        'product': product,
    }
    return render(request, 'products/product_confirm_delete.html', context)