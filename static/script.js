class ShoppingCart {
    constructor() {
        this.products = [];
        this.cart = this.loadCartFromStorage();
        this.initializeElements();
        this.bindEvents();
        this.loadProducts();
        this.updateCartDisplay();
    }

    initializeElements() {
        this.elements = {
            productsGrid: document.getElementById('productsGrid'),
            loading: document.getElementById('loading'),
            cartBtn: document.getElementById('cartBtn'),
            cartCount: document.getElementById('cartCount'),
            cartModal: document.getElementById('cartModal'),
            cartItems: document.getElementById('cartItems'),
            cartTotal: document.getElementById('cartTotal'),
            closeCartBtn: document.getElementById('closeCartBtn'),
            continueShopping: document.getElementById('continueShopping'),
            checkoutBtn: document.getElementById('checkoutBtn'),
            successModal: document.getElementById('successModal'),
            successMessage: document.getElementById('successMessage'),
            closeSuccessBtn: document.getElementById('closeSuccessBtn'),
            closeSuccessOk: document.getElementById('closeSuccessOk')
        };
    }

    bindEvents() {
        this.elements.cartBtn.addEventListener('click', () => this.showCart());
        this.elements.closeCartBtn.addEventListener('click', () => this.hideCart());
        this.elements.continueShopping.addEventListener('click', () => this.hideCart());
        this.elements.checkoutBtn.addEventListener('click', () => this.checkout());
        this.elements.closeSuccessBtn.addEventListener('click', () => this.hideSuccess());
        this.elements.closeSuccessOk.addEventListener('click', () => this.hideSuccess());

        // Close modals when clicking outside
        this.elements.cartModal.addEventListener('click', (e) => {
            if (e.target === this.elements.cartModal) this.hideCart();
        });
        this.elements.successModal.addEventListener('click', (e) => {
            if (e.target === this.elements.successModal) this.hideSuccess();
        });
    }

    async loadProducts() {
        try {
            this.elements.loading.style.display = 'block';
            const response = await fetch('/products');
            if (!response.ok) throw new Error('Failed to load products');
            
            this.products = await response.json();
            this.renderProducts();
        } catch (error) {
            console.error('Error loading products:', error);
            this.elements.productsGrid.innerHTML = '<p class="error">Failed to load products. Please try again.</p>';
        } finally {
            this.elements.loading.style.display = 'none';
        }
    }

    renderProducts() {
        this.elements.productsGrid.innerHTML = this.products.map(product => `
            <div class="product-card">
                <img src="${product.imageUrl}" alt="${product.name}" class="product-image">
                <div class="product-info">
                    <h3 class="product-name">${product.name}</h3>
                    <p class="product-price">₹${product.price.toFixed(2)}</p>
                    <button class="add-to-cart-btn" onclick="cart.addToCart(${product.id})">
                        Add to Cart
                    </button>
                </div>
            </div>
        `).join('');
    }

    addToCart(productId) {
        const product = this.products.find(p => p.id === productId);
        if (!product) return;

        const existingItem = this.cart.find(item => item.productId === productId);
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            this.cart.push({ productId, quantity: 1 });
        }

        this.saveCartToStorage();
        this.updateCartDisplay();
        this.showCartAddedFeedback();
    }

    removeFromCart(productId) {
        this.cart = this.cart.filter(item => item.productId !== productId);
        this.saveCartToStorage();
        this.updateCartDisplay();
        this.renderCartItems();
    }

    updateQuantity(productId, newQuantity) {
        if (newQuantity <= 0) {
            this.removeFromCart(productId);
            return;
        }

        const item = this.cart.find(item => item.productId === productId);
        if (item) {
            item.quantity = newQuantity;
            this.saveCartToStorage();
            this.updateCartDisplay();
            this.renderCartItems();
        }
    }

    getCartTotal() {
        return this.cart.reduce((total, item) => {
            const product = this.products.find(p => p.id === item.productId);
            return total + (product ? product.price * item.quantity : 0);
        }, 0);
    }

    getCartItemCount() {
        return this.cart.reduce((count, item) => count + item.quantity, 0);
    }

    updateCartDisplay() {
        this.elements.cartCount.textContent = this.getCartItemCount();
        this.elements.cartTotal.textContent = this.getCartTotal().toFixed(2);
        
        // Enable/disable checkout button
        this.elements.checkoutBtn.disabled = this.cart.length === 0;
    }

    renderCartItems() {
        if (this.cart.length === 0) {
            this.elements.cartItems.innerHTML = '<div class="empty-cart">Your cart is empty</div>';
            return;
        }

        this.elements.cartItems.innerHTML = this.cart.map(item => {
            const product = this.products.find(p => p.id === item.productId);
            if (!product) return '';

            return `
                <div class="cart-item">
                    <img src="${product.imageUrl}" alt="${product.name}" class="cart-item-image">
                    <div class="cart-item-info">
                        <div class="cart-item-name">${product.name}</div>
                        <div class="cart-item-price">₹${product.price.toFixed(2)} each</div>
                    </div>
                    <div class="quantity-controls">
                        <button class="quantity-btn" onclick="cart.updateQuantity(${product.id}, ${item.quantity - 1})" ${item.quantity <= 1 ? 'disabled' : ''}>-</button>
                        <span class="quantity">${item.quantity}</span>
                        <button class="quantity-btn" onclick="cart.updateQuantity(${product.id}, ${item.quantity + 1})">+</button>
                    </div>
                    <button class="remove-btn" onclick="cart.removeFromCart(${product.id})">Remove</button>
                </div>
            `;
        }).join('');
    }

    showCart() {
        this.renderCartItems();
        this.elements.cartModal.classList.add('show');
    }

    hideCart() {
        this.elements.cartModal.classList.remove('show');
    }

    showSuccess(message) {
        this.elements.successMessage.textContent = message;
        this.elements.successModal.classList.add('show');
    }

    hideSuccess() {
        this.elements.successModal.classList.remove('show');
    }

    showCartAddedFeedback() {
        const cartBtn = this.elements.cartBtn;
        const originalText = cartBtn.textContent;
        cartBtn.textContent = '✓ Added to Cart!';
        cartBtn.style.background = '#10b981';
        
        setTimeout(() => {
            cartBtn.textContent = originalText;
            cartBtn.style.background = '#2563eb';
        }, 1000);
    }

    async checkout() {
        if (this.cart.length === 0) return;

        try {
            this.elements.checkoutBtn.disabled = true;
            this.elements.checkoutBtn.textContent = 'Processing...';

            const response = await fetch('/checkout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    items: this.cart.map(item => ({
                        productId: item.productId,
                        quantity: item.quantity
                    }))
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Checkout failed');
            }

            const result = await response.json();
            
            // Clear cart and update display
            this.cart = [];
            this.saveCartToStorage();
            this.updateCartDisplay();
            this.hideCart();
            
            // Show success message
            this.showSuccess(result.message);

        } catch (error) {
            console.error('Checkout error:', error);
            alert(`Checkout failed: ${error.message}`);
        } finally {
            this.elements.checkoutBtn.disabled = false;
            this.elements.checkoutBtn.textContent = 'Checkout';
        }
    }

    saveCartToStorage() {
        localStorage.setItem('shoppingCart', JSON.stringify(this.cart));
    }

    loadCartFromStorage() {
        try {
            const saved = localStorage.getItem('shoppingCart');
            return saved ? JSON.parse(saved) : [];
        } catch (error) {
            console.error('Error loading cart from storage:', error);
            return [];
        }
    }
}

// Initialize the shopping cart when the page loads
const cart = new ShoppingCart();
// Make cart available globally for inline event handlers
window.cart = cart;