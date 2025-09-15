from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Cart, CartItem
from products.models import Product

@login_required
def check_cart_status(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = [{'product_id': item.product.id, 'quantity': item.quantity} for item in cart.items.all()]
    return JsonResponse({
        'total_items': cart.get_total_items(),
        'total_price': cart.get_total_price(),
        'cart_items': cart_items
    })

@login_required
def cart_detail(request):
    # Get or create cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if product is available
    if not product.is_available():
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': f"{product.name} is out of stock."
            })
        messages.error(request, f"{product.name} is out of stock.")
        return redirect('product_detail', pk=product_id)
    
    # Get quantity from form, default to 1
    # Handle both GET and POST requests
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
    else:  # GET request from direct link
        quantity = int(request.GET.get('quantity', 1))
    
    # Validate quantity
    if quantity <= 0:
        quantity = 1
    if quantity > product.inventory:
        quantity = product.inventory
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f"Only {product.inventory} units of {product.name} available. Adjusted quantity.",
                'quantity': quantity
            })
        messages.warning(request, f"Only {product.inventory} units of {product.name} available. Adjusted quantity.")
    
    # Get or create cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Try to get existing cart item or create new one
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        # Update quantity, ensuring it doesn't exceed inventory
        new_quantity = cart_item.quantity + quantity
        if new_quantity > product.inventory:
            new_quantity = product.inventory
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f"Cart adjusted to maximum available quantity ({product.inventory}).",
                    'total_items': cart.get_total_items(),
                    'total_price': cart.get_total_price(),
                    'product_name': product.name
                })
            messages.warning(request, f"Cart adjusted to maximum available quantity ({product.inventory}).")
        cart_item.quantity = new_quantity
        cart_item.save()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f"Updated {product.name} quantity in your cart.",
                'total_items': cart.get_total_items(),
                'total_price': cart.get_total_price(),
                'product_name': product.name
            })
        messages.success(request, f"Updated {product.name} quantity in your cart.")
    except CartItem.DoesNotExist:
        CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f"Added {product.name} to your cart.",
                'total_items': cart.get_total_items(),
                'total_price': cart.get_total_price(),
                'product_name': product.name
            })
        messages.success(request, f"Added {product.name} to your cart.")
    
    return redirect('cart_detail')

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    action = request.POST.get('action')
    if action == 'remove':
        cart_item.delete()
        messages.success(request, f"Removed {cart_item.product.name} from your cart.")
    else:
        # Get new quantity
        try:
            quantity = int(request.POST.get('quantity', cart_item.quantity))
            if quantity <= 0:
                cart_item.delete()
                messages.success(request, f"Removed {cart_item.product.name} from your cart.")
            else:
                # Check inventory
                if quantity > cart_item.product.inventory:
                    quantity = cart_item.product.inventory
                    messages.warning(request, f"Only {cart_item.product.inventory} units available. Adjusted quantity.")
                
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, f"Updated {cart_item.product.name} quantity.")
        except ValueError:
            messages.error(request, "Invalid quantity.")
    
    # Handle AJAX requests
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart = Cart.objects.get(user=request.user)
        # Include item price if the item still exists
        item_price = None
        try:
            updated_item = CartItem.objects.get(id=item_id)
            item_price = updated_item.get_cost()
        except CartItem.DoesNotExist:
            # Item was removed
            pass
            
        return JsonResponse({
            'success': True,
            'total_price': cart.get_total_price(),
            'total_items': cart.get_total_items(),
            'item_price': item_price
        })
    
    return redirect('cart_detail')

@login_required
def clear_cart(request):
    if request.method == 'POST':
        try:
            cart = Cart.objects.get(user=request.user)
            cart.clear()
            messages.success(request, "Your cart has been cleared.")
        except Cart.DoesNotExist:
            pass
    
    return redirect('cart_detail')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    # Check if cart is empty
    if len(cart.get_cart_items()) == 0:
        messages.warning(request, "Your cart is empty. Add some products before checkout.")
        return redirect('product_list')
    
    if request.method == 'POST':
        # Process checkout
        # Check inventory and availability before finalizing
        inventory_error = False
        for item in cart.get_cart_items():
            if not item.product.is_available():
                messages.error(request, f"{item.product.name} is no longer available.")
                inventory_error = True
            elif item.quantity > item.product.inventory:
                messages.error(request, f"Sorry, only {item.product.inventory} units of {item.product.name} available.")
                inventory_error = True
        
        if inventory_error:
            return redirect('cart_detail')
        
        # Update inventory using the update_stock method
        for item in cart.get_cart_items():
            product = item.product
            product.update_stock(-item.quantity)
        
        # Clear cart after successful checkout
        cart.clear()
        
        messages.success(request, "Your order has been placed successfully!")
        return redirect('product_list')
    
    return render(request, 'cart/checkout.html', {'cart': cart})