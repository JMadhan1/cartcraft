class CartCraft {
    constructor() {
        this.products = [];
        this.filteredProducts = [];
        this.cart = this.loadCartFromStorage();
        this.wishlist = this.loadWishlistFromStorage();
        this.darkMode = this.loadThemeFromStorage();
        this.currentView = 'grid';
        
        this.initializeElements();
        this.bindEvents();
        this.loadProducts();
        this.updateCartDisplay();
        this.updateWishlistDisplay();
        this.applyTheme();
    }

    initializeElements() {
        this.elements = {
            // Header elements
            searchInput: document.getElementById('searchInput'),
            searchClear: document.getElementById('searchClear'),
            categoryFilter: document.getElementById('categoryFilter'),
            themeToggle: document.getElementById('themeToggle'),
            wishlistBtn: document.getElementById('wishlistBtn'),
            wishlistCount: document.getElementById('wishlistCount'),
            cartBtn: document.getElementById('cartBtn'),
            cartCount: document.getElementById('cartCount'),
            
            // Main content
            loading: document.getElementById('loading'),
            resultsInfo: document.getElementById('resultsInfo'),
            resultsCount: document.getElementById('resultsCount'),
            productsGrid: document.getElementById('productsGrid'),
            noResults: document.getElementById('noResults'),
            
            // Cart modal
            cartModal: document.getElementById('cartModal'),
            cartItems: document.getElementById('cartItems'),
            subtotal: document.getElementById('subtotal'),
            tax: document.getElementById('tax'),
            cartTotal: document.getElementById('cartTotal'),
            promoInput: document.getElementById('promoInput'),
            closeCartBtn: document.getElementById('closeCartBtn'),
            continueShopping: document.getElementById('continueShopping'),
            checkoutBtn: document.getElementById('checkoutBtn'),
            
            // Wishlist modal
            wishlistModal: document.getElementById('wishlistModal'),
            wishlistItems: document.getElementById('wishlistItems'),
            closeWishlistBtn: document.getElementById('closeWishlistBtn'),
            closeWishlist: document.getElementById('closeWishlist'),
            addAllToCart: document.getElementById('addAllToCart'),
            
            // Quick view modal
            quickViewModal: document.getElementById('quickViewModal'),
            quickViewContent: document.getElementById('quickViewContent'),
            closeQuickViewBtn: document.getElementById('closeQuickViewBtn'),
            
            // Success modal
            successModal: document.getElementById('successModal'),
            successMessage: document.getElementById('successMessage'),
            closeSuccessBtn: document.getElementById('closeSuccessBtn'),
            trackOrder: document.getElementById('trackOrder'),
            continueBrowsing: document.getElementById('continueBrowsing'),
            
            // Toast container
            toastContainer: document.getElementById('toastContainer')
        };
    }

    bindEvents() {
        // Search and filter
        this.elements.searchInput.addEventListener('input', (e) => this.handleSearch(e.target.value));
        this.elements.searchClear.addEventListener('click', () => this.clearSearch());
        this.elements.categoryFilter.addEventListener('change', (e) => this.handleCategoryFilter(e.target.value));
        
        // Theme toggle
        this.elements.themeToggle.addEventListener('click', () => this.toggleTheme());
        
        // Header buttons
        this.elements.wishlistBtn.addEventListener('click', () => this.showWishlist());
        this.elements.cartBtn.addEventListener('click', () => this.showCart());
        
        // View options
        document.querySelectorAll('.view-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.changeView(e.target.closest('.view-btn').dataset.view));
        });
        
        // Modal close events
        this.elements.closeCartBtn.addEventListener('click', () => this.hideCart());
        this.elements.continueShopping.addEventListener('click', () => this.hideCart());
        this.elements.checkoutBtn.addEventListener('click', () => this.checkout());
        
        this.elements.closeWishlistBtn.addEventListener('click', () => this.hideWishlist());
        this.elements.closeWishlist.addEventListener('click', () => this.hideWishlist());
        this.elements.addAllToCart.addEventListener('click', () => this.addAllWishlistToCart());
        
        this.elements.closeQuickViewBtn.addEventListener('click', () => this.hideQuickView());
        
        this.elements.closeSuccessBtn.addEventListener('click', () => this.hideSuccess());
        this.elements.trackOrder.addEventListener('click', () => this.trackOrder());
        this.elements.continueBrowsing.addEventListener('click', () => this.hideSuccess());
        
        // Promo code
        document.querySelector('.apply-promo').addEventListener('click', () => this.applyPromoCode());
        
        // Modal overlay clicks
        [this.elements.cartModal, this.elements.wishlistModal, this.elements.quickViewModal, this.elements.successModal].forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.classList.remove('show');
                }
            });
        });
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));
    }

    async loadProducts() {
        try {
            console.log('Starting to load products...');
            this.elements.loading.style.display = 'flex';
            this.elements.productsGrid.style.display = 'none';
            this.elements.noResults.style.display = 'none';
            
            const response = await fetch('/products');
            console.log('Response status:', response.status);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const products = await response.json();
            console.log('Products received:', products.length, 'products');
            
            if (!Array.isArray(products)) {
                throw new Error('Invalid response format - expected array');
            }
            
            this.products = products;
            this.filteredProducts = [...this.products];
            this.renderProducts();
            this.updateResultsInfo();
            
            console.log('Products loaded and rendered successfully');
        } catch (error) {
            console.error('Error loading products:', error);
            this.elements.noResults.style.display = 'block';
            this.elements.noResults.innerHTML = `
                <div class="empty-cart">
                    <i class="fas fa-exclamation-triangle"></i>
                    <h3>Failed to load products</h3>
                    <p>Error: ${error.message}</p>
                    <button onclick="cart.loadProducts()" class="btn btn-primary">Retry</button>
                </div>
            `;
            this.showToast('Error loading products. Please try again.', 'error');
        } finally {
            this.elements.loading.style.display = 'none';
            this.elements.productsGrid.style.display = 'grid';
        }
    }

    renderProducts() {
        const container = this.elements.productsGrid;
        
        console.log('Rendering products:', this.filteredProducts.length, 'products');
        
        if (!this.filteredProducts || this.filteredProducts.length === 0) {
            console.log('No products to display');
            this.elements.noResults.style.display = 'block';
            container.style.display = 'none';
            return;
        }
        
        this.elements.noResults.style.display = 'none';
        container.style.display = 'grid';
        
        container.innerHTML = this.filteredProducts.map(product => `
            <div class="product-card animate-fade-in" data-product-id="${product.id}">
                <div class="product-image-container">
                    <img src="${product.imageUrl}" alt="${product.name}" class="product-image" loading="lazy">
                    <div class="product-badge badge-${product.badge.toLowerCase().replace(' ', '-')}">${product.badge}</div>
                    <div class="product-actions">
                        <button class="action-btn wishlist-toggle ${this.isInWishlist(product.id) ? 'active' : ''}" 
                                onclick="cart.toggleWishlist(${product.id})" title="Add to wishlist">
                            <i class="fas fa-heart"></i>
                        </button>
                        <button class="action-btn quick-view" onclick="cart.showQuickView(${product.id})" title="Quick view">
                            <i class="fas fa-eye"></i>
                        </button>
                    </div>
                </div>
                <div class="product-info">
                    <div class="product-brand">${product.brand}</div>
                    <h3 class="product-name">${product.name}</h3>
                    <div class="product-rating">
                        <div class="stars">
                            ${this.renderStars(product.rating)}
                        </div>
                        <span class="rating-text">${product.rating} (${product.reviews.toLocaleString('en-IN')})</span>
                    </div>
                    <div class="product-pricing">
                        <span class="product-price">₹${product.price.toLocaleString('en-IN')}</span>
                        <span class="original-price">₹${product.originalPrice.toLocaleString('en-IN')}</span>
                        <span class="discount">${product.discount}</span>
                    </div>
                    <button class="add-to-cart-btn" onclick="cart.addToCart(${product.id})">
                        <i class="fas fa-shopping-cart"></i>
                        Add to Cart
                    </button>
                </div>
            </div>
        `).join('');
    }

    renderStars(rating) {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 !== 0;
        const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
        
        return [
            ...Array(fullStars).fill('<i class="fas fa-star star"></i>'),
            ...(hasHalfStar ? ['<i class="fas fa-star-half-alt star"></i>'] : []),
            ...Array(emptyStars).fill('<i class="far fa-star star"></i>')
        ].join('');
    }

    handleSearch(query) {
        const searchTerm = query.toLowerCase().trim();
        
        if (searchTerm) {
            this.elements.searchClear.style.display = 'block';
        } else {
            this.elements.searchClear.style.display = 'none';
        }
        
        this.filterProducts();
    }

    clearSearch() {
        this.elements.searchInput.value = '';
        this.elements.searchClear.style.display = 'none';
        this.filterProducts();
    }

    handleCategoryFilter(category) {
        this.filterProducts();
    }

    filterProducts() {
        const searchTerm = this.elements.searchInput.value.toLowerCase().trim();
        const selectedCategory = this.elements.categoryFilter.value;
        
        this.filteredProducts = this.products.filter(product => {
            const matchesSearch = !searchTerm || 
                product.name.toLowerCase().includes(searchTerm) ||
                product.brand.toLowerCase().includes(searchTerm) ||
                product.description.toLowerCase().includes(searchTerm);
            
            const matchesCategory = !selectedCategory || product.category === selectedCategory;
            
            return matchesSearch && matchesCategory;
        });
        
        this.renderProducts();
        this.updateResultsInfo();
    }

    updateResultsInfo() {
        const count = this.filteredProducts.length;
        this.elements.resultsCount.textContent = `${count} product${count !== 1 ? 's' : ''} found`;
    }

    changeView(view) {
        this.currentView = view;
        document.querySelectorAll('.view-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelector(`[data-view="${view}"]`).classList.add('active');
        
        if (view === 'list') {
            this.elements.productsGrid.classList.add('list-view');
        } else {
            this.elements.productsGrid.classList.remove('list-view');
        }
    }

    // Wishlist functionality
    toggleWishlist(productId) {
        const product = this.products.find(p => p.id === productId);
        if (!product) return;
        
        const isInWishlist = this.isInWishlist(productId);
        
        if (isInWishlist) {
            this.wishlist = this.wishlist.filter(id => id !== productId);
            this.showToast(`${product.name} removed from wishlist`, 'info');
        } else {
            this.wishlist.push(productId);
            this.showToast(`${product.name} added to wishlist`, 'success');
        }
        
        this.saveWishlistToStorage();
        this.updateWishlistDisplay();
        this.renderProducts(); // Re-render to update heart icons
    }

    isInWishlist(productId) {
        return this.wishlist.includes(productId);
    }

    updateWishlistDisplay() {
        this.elements.wishlistCount.textContent = this.wishlist.length;
    }

    showWishlist() {
        this.renderWishlistItems();
        this.elements.wishlistModal.classList.add('show');
    }

    hideWishlist() {
        this.elements.wishlistModal.classList.remove('show');
    }

    renderWishlistItems() {
        const wishlistProducts = this.products.filter(p => this.wishlist.includes(p.id));
        
        if (wishlistProducts.length === 0) {
            this.elements.wishlistItems.innerHTML = `
                <div class="empty-cart">
                    <i class="fas fa-heart-broken"></i>
                    <h3>Your wishlist is empty</h3>
                    <p>Start adding products you love!</p>
                </div>
            `;
            return;
        }
        
        this.elements.wishlistItems.innerHTML = wishlistProducts.map(product => `
            <div class="cart-item">
                <img src="${product.imageUrl}" alt="${product.name}" class="cart-item-image">
                <div class="cart-item-info">
                    <div class="cart-item-name">${product.name}</div>
                    <div class="cart-item-price">₹${product.price.toLocaleString('en-IN')}</div>
                </div>
                <button class="btn btn-primary" onclick="cart.addToCart(${product.id})">
                    <i class="fas fa-shopping-cart"></i> Add to Cart
                </button>
                <button class="remove-btn" onclick="cart.toggleWishlist(${product.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `).join('');
    }

    addAllWishlistToCart() {
        let addedCount = 0;
        this.wishlist.forEach(productId => {
            const existingItem = this.cart.find(item => item.productId === productId);
            if (!existingItem) {
                this.cart.push({ productId, quantity: 1 });
                addedCount++;
            }
        });
        
        if (addedCount > 0) {
            this.saveCartToStorage();
            this.updateCartDisplay();
            this.showToast(`${addedCount} item${addedCount !== 1 ? 's' : ''} added to cart`, 'success');
            this.hideWishlist();
        } else {
            this.showToast('All wishlist items are already in your cart', 'info');
        }
    }

    // Quick view functionality
    showQuickView(productId) {
        const product = this.products.find(p => p.id === productId);
        if (!product) return;
        
        this.elements.quickViewContent.innerHTML = `
            <div class="quick-view-product">
                <div class="quick-view-image">
                    <img src="${product.imageUrl}" alt="${product.name}">
                    <div class="product-badge badge-${product.badge.toLowerCase().replace(' ', '-')}">${product.badge}</div>
                </div>
                <div class="quick-view-info">
                    <div class="product-brand">${product.brand}</div>
                    <h2>${product.name}</h2>
                    <div class="product-rating">
                        <div class="stars">${this.renderStars(product.rating)}</div>
                        <span class="rating-text">${product.rating} (${product.reviews.toLocaleString('en-IN')} reviews)</span>
                    </div>
                    <p class="product-description">${product.description}</p>
                    <div class="product-pricing">
                        <span class="product-price">₹${product.price.toLocaleString('en-IN')}</span>
                        <span class="original-price">₹${product.originalPrice.toLocaleString('en-IN')}</span>
                        <span class="discount">${product.discount}</span>
                    </div>
                    <div class="quick-view-actions">
                        <button class="btn btn-outline wishlist-toggle ${this.isInWishlist(product.id) ? 'active' : ''}" 
                                onclick="cart.toggleWishlist(${product.id})">
                            <i class="fas fa-heart"></i> ${this.isInWishlist(product.id) ? 'Remove from' : 'Add to'} Wishlist
                        </button>
                        <button class="btn btn-primary" onclick="cart.addToCart(${product.id}); cart.hideQuickView();">
                            <i class="fas fa-shopping-cart"></i> Add to Cart
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        this.elements.quickViewModal.classList.add('show');
    }

    hideQuickView() {
        this.elements.quickViewModal.classList.remove('show');
    }

    // Theme functionality
    toggleTheme() {
        this.darkMode = !this.darkMode;
        this.applyTheme();
        this.saveThemeToStorage();
    }

    applyTheme() {
        const body = document.body;
        const icon = this.elements.themeToggle.querySelector('i');
        
        if (this.darkMode) {
            body.classList.add('dark-theme');
            icon.className = 'fas fa-sun';
        } else {
            body.classList.remove('dark-theme');
            icon.className = 'fas fa-moon';
        }
    }

    // Cart functionality (enhanced)
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
        this.showToast(`${product.name} added to cart!`, 'success');
    }

    removeFromCart(productId) {
        const product = this.products.find(p => p.id === productId);
        this.cart = this.cart.filter(item => item.productId !== productId);
        this.saveCartToStorage();
        this.updateCartDisplay();
        this.renderCartItems();
        this.showToast(`${product.name} removed from cart`, 'info');
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
        const subtotal = this.getCartTotal();
        const tax = Math.round(subtotal * 0.18); // 18% GST
        const total = subtotal + tax;
        
        this.elements.cartCount.textContent = this.getCartItemCount();
        this.elements.subtotal.textContent = `₹${subtotal.toLocaleString('en-IN')}`;
        this.elements.tax.textContent = `₹${tax.toLocaleString('en-IN')}`;
        this.elements.cartTotal.textContent = `₹${total.toLocaleString('en-IN')}`;
        
        this.elements.checkoutBtn.disabled = this.cart.length === 0;
    }

    renderCartItems() {
        if (this.cart.length === 0) {
            this.elements.cartItems.innerHTML = `
                <div class="empty-cart">
                    <i class="fas fa-shopping-cart"></i>
                    <h3>Your cart is empty</h3>
                    <p>Start shopping to add items to your cart!</p>
                </div>
            `;
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
                        <div class="cart-item-price">₹${product.price.toLocaleString('en-IN')} each</div>
                    </div>
                    <div class="quantity-controls">
                        <button class="quantity-btn" onclick="cart.updateQuantity(${product.id}, ${item.quantity - 1})" ${item.quantity <= 1 ? 'disabled' : ''}>
                            <i class="fas fa-minus"></i>
                        </button>
                        <span class="quantity">${item.quantity}</span>
                        <button class="quantity-btn" onclick="cart.updateQuantity(${product.id}, ${item.quantity + 1})">
                            <i class="fas fa-plus"></i>
                        </button>
                    </div>
                    <button class="remove-btn" onclick="cart.removeFromCart(${product.id})">
                        <i class="fas fa-trash"></i>
                    </button>
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

    showCartAddedFeedback() {
        const cartBtn = this.elements.cartBtn;
        const originalContent = cartBtn.innerHTML;
        
        cartBtn.innerHTML = '<i class="fas fa-check"></i> Added!';
        cartBtn.style.background = 'var(--success-gradient)';
        
        setTimeout(() => {
            cartBtn.innerHTML = originalContent;
            cartBtn.style.background = 'var(--primary-gradient)';
        }, 1500);
    }

    applyPromoCode() {
        const code = this.elements.promoInput.value.trim();
        if (!code) {
            this.showToast('Please enter a promo code', 'warning');
            return;
        }
        
        // Simulate promo code validation
        const validCodes = ['SAVE10', 'WELCOME20', 'FIRST50'];
        if (validCodes.includes(code.toUpperCase())) {
            this.showToast(`Promo code ${code.toUpperCase()} applied successfully!`, 'success');
            this.elements.promoInput.value = '';
        } else {
            this.showToast('Invalid promo code', 'error');
        }
    }

    async checkout() {
        if (this.cart.length === 0) return;

        try {
            this.elements.checkoutBtn.disabled = true;
            this.elements.checkoutBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';

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
            
            // Show success with animation
            this.showSuccess(result.message);
            
            // Trigger confetti animation
            this.triggerConfetti();

        } catch (error) {
            console.error('Checkout error:', error);
            this.showToast(`Checkout failed: ${error.message}`, 'error');
        } finally {
            this.elements.checkoutBtn.disabled = false;
            this.elements.checkoutBtn.innerHTML = '<i class="fas fa-credit-card"></i> Secure Checkout';
        }
    }

    showSuccess(message) {
        this.elements.successMessage.textContent = message;
        this.elements.successModal.classList.add('show');
    }

    hideSuccess() {
        this.elements.successModal.classList.remove('show');
    }

    trackOrder() {
        this.showToast('Redirecting to order tracking...', 'info');
        this.hideSuccess();
    }

    triggerConfetti() {
        // Add confetti animation effect
        const confetti = document.querySelector('.confetti');
        if (confetti) {
            confetti.style.animation = 'none';
            setTimeout(() => {
                confetti.style.animation = 'confetti 2s ease-in-out infinite';
            }, 100);
        }
    }

    // Toast notification system
    showToast(message, type = 'info', duration = 4000) {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        };
        
        toast.innerHTML = `
            <i class="toast-icon ${icons[type]}"></i>
            <div class="toast-content">
                <div class="toast-message">${message}</div>
            </div>
            <button class="toast-close">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        // Close button functionality
        toast.querySelector('.toast-close').addEventListener('click', () => {
            this.removeToast(toast);
        });
        
        // Add to container
        this.elements.toastContainer.appendChild(toast);
        
        // Trigger show animation
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Auto-remove after duration
        setTimeout(() => this.removeToast(toast), duration);
    }

    removeToast(toast) {
        toast.classList.remove('show');
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }

    // Keyboard shortcuts
    handleKeyboard(e) {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
        
        switch (e.key) {
            case 'Escape':
                // Close any open modals
                document.querySelectorAll('.modal-overlay.show').forEach(modal => {
                    modal.classList.remove('show');
                });
                break;
            case '/':
                e.preventDefault();
                this.elements.searchInput.focus();
                break;
            case 'c':
                if (e.ctrlKey || e.metaKey) return; // Don't interfere with copy
                this.showCart();
                break;
            case 'w':
                if (e.ctrlKey || e.metaKey) return; // Don't interfere with close tab
                this.showWishlist();
                break;
            case 't':
                if (e.ctrlKey || e.metaKey) return; // Don't interfere with new tab
                this.toggleTheme();
                break;
        }
    }

    // Local storage functions
    saveCartToStorage() {
        localStorage.setItem('cartcraft_cart', JSON.stringify(this.cart));
    }

    loadCartFromStorage() {
        try {
            const saved = localStorage.getItem('cartcraft_cart');
            return saved ? JSON.parse(saved) : [];
        } catch (error) {
            console.error('Error loading cart from storage:', error);
            return [];
        }
    }

    saveWishlistToStorage() {
        localStorage.setItem('cartcraft_wishlist', JSON.stringify(this.wishlist));
    }

    loadWishlistFromStorage() {
        try {
            const saved = localStorage.getItem('cartcraft_wishlist');
            return saved ? JSON.parse(saved) : [];
        } catch (error) {
            console.error('Error loading wishlist from storage:', error);
            return [];
        }
    }

    saveThemeToStorage() {
        localStorage.setItem('cartcraft_theme', JSON.stringify(this.darkMode));
    }

    loadThemeFromStorage() {
        try {
            const saved = localStorage.getItem('cartcraft_theme');
            return saved ? JSON.parse(saved) : false;
        } catch (error) {
            console.error('Error loading theme from storage:', error);
            return false;
        }
    }
}

// Initialize the application when the page loads
const cart = new CartCraft();
// Make cart available globally for inline event handlers
window.cart = cart;