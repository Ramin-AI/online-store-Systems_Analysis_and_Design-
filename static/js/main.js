// Main JavaScript file for the Online Store application

document.addEventListener('DOMContentLoaded', function() {
    // Handle quantity changes in cart
    const quantityInputs = document.querySelectorAll('.cart-item-quantity input');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const form = this.closest('form');
            form.submit();
        });
    });

    // Handle quantity increment/decrement buttons
    const quantityButtons = document.querySelectorAll('.quantity-btn');
    quantityButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const input = this.parentNode.querySelector('input');
            const currentValue = parseInt(input.value);
            
            if (this.classList.contains('increment') && currentValue < parseInt(input.max)) {
                input.value = currentValue + 1;
            } else if (this.classList.contains('decrement') && currentValue > parseInt(input.min)) {
                input.value = currentValue - 1;
            }
            
            // Trigger change event to submit the form
            const event = new Event('change');
            input.dispatchEvent(event);
        });
    });

    // Handle Add to Cart buttons with AJAX
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    
    // Check if products are in cart on page load
    function checkCartStatus() {
        fetch('/cart/check-status/', {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.cart_items) {
                // Update buttons for products that are in the cart
                data.cart_items.forEach(item => {
                    const button = document.querySelector(`.add-to-cart-btn[data-product-id="${item.product_id}"]`);
                    if (button) {
                        button.textContent = 'Added to Cart';
                        button.classList.add('added');
                    }
                });
            }
        })
        .catch(error => console.error('Error checking cart status:', error));
    }
    
    // Call on page load
    checkCartStatus();
    
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Check if the button is already in 'added' state
            if (this.classList.contains('added')) {
                // Do nothing if the button is already in 'Added to Cart' state
                return;
            }
            
            const productId = this.getAttribute('data-product-id');
            const url = this.getAttribute('href');
            
            // Change button text to indicate loading
            this.textContent = 'Adding...';
            this.classList.add('loading');
            
            // Send AJAX request to add item to cart
            fetch(url, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update cart count in the header
                    let cartCount = document.querySelector('.cart-count');
                    const cartIcon = document.querySelector('.cart-icon');
                    
                    if (!cartCount && cartIcon && data.total_items > 0) {
                        // Create the cart count element if it doesn't exist
                        cartCount = document.createElement('span');
                        cartCount.className = 'cart-count';
                        cartIcon.appendChild(cartCount);
                    }
                    
                    if (cartCount) {
                        cartCount.textContent = data.total_items;
                        cartCount.classList.add('updated');
                        setTimeout(() => cartCount.classList.remove('updated'), 1000);
                    }
                    
                    // Change button to indicate success
                    this.textContent = 'Added to Cart';
                    this.classList.remove('loading');
                    this.classList.add('added');
                    
                    // Show success message for cart operations
                    showMessage('success', data.message || `Added ${data.product_name} to your cart.`);
                }
                else {
                    // Show error message
                    this.textContent = 'Add to Cart';
                    this.classList.remove('loading');
                    showMessage('error', data.message || 'Error adding item to cart.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                this.textContent = 'Add to Cart';
                this.classList.remove('loading');
                showMessage('error', 'Error adding item to cart.');
            });
        });
    });

    // Product card quantity controls
    const productQuantityControls = document.querySelectorAll('.product-quantity-controls');
    productQuantityControls.forEach(control => {
        const decreaseBtn = control.querySelector('.decrease-btn');
        const increaseBtn = control.querySelector('.increase-btn');
        const quantityInput = control.querySelector('.quantity-input');
        const maxQuantity = parseInt(quantityInput.getAttribute('max') || 99);
        
        decreaseBtn.addEventListener('click', function() {
            let currentValue = parseInt(quantityInput.value);
            if (currentValue > 1) {
                quantityInput.value = currentValue - 1;
            }
        });
        
        increaseBtn.addEventListener('click', function() {
            let currentValue = parseInt(quantityInput.value);
            if (currentValue < maxQuantity) {
                quantityInput.value = currentValue + 1;
            }
        });
    });

    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.message');
    if (messages.length > 0) {
        setTimeout(function() {
            messages.forEach(message => {
                message.style.opacity = '0';
                setTimeout(function() {
                    message.style.display = 'none';
                }, 500);
            });
        }, 5000);
    }
    
    // Function to show messages - disabled as per requirement
    function showMessage(type, text) {
        // Do not display any messages
        return;
        
        // The code below is disabled
        /*
        const messagesContainer = document.querySelector('.messages');
        if (!messagesContainer) {
            const main = document.querySelector('main');
            const newMessagesContainer = document.createElement('div');
            newMessagesContainer.className = 'messages';
            main.insertBefore(newMessagesContainer, main.firstChild);
        }
        
        const messageElement = document.createElement('div');
        messageElement.className = `message ${type}`;
        messageElement.textContent = text;
        
        const container = document.querySelector('.messages') || newMessagesContainer;
        container.appendChild(messageElement);
        
        // Auto-hide after 5 seconds
        setTimeout(function() {
            messageElement.style.opacity = '0';
            setTimeout(function() {
                messageElement.remove();
            }, 500);
        }, 5000);
        */
    }
});