from .models import Cart

def cart_processor(request):
    """
    Context processor to make cart data available to all templates.
    """
    if request.user.is_authenticated:
        # Get or create cart for the user
        cart, created = Cart.objects.get_or_create(user=request.user)
        return {
            'cart': cart,
            'cart_total_items': cart.get_total_items(),
            'cart_total_price': cart.get_total_price()
        }
    return {'cart': None, 'cart_total_items': 0, 'cart_total_price': 0}