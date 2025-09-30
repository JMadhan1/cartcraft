from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import datetime
import uuid

app = Flask(__name__, static_folder='static')

# Enable CORS for frontend communication
CORS(app)

# Realistic Indian e-commerce product data with authentic pricing and categories
PRODUCTS = [
    # Electronics Category (6 items)
    {
        "id": 1,
        "name": "iPhone 14 Pro Max",
        "price": 129900,
        "originalPrice": 139900,
        "discount": "7% OFF",
        "category": "Electronics",
        "brand": "Apple",
        "rating": 4.6,
        "reviews": 15420,
        "badge": "Best Seller",
        "description": "Latest iPhone with A16 Bionic chip, Pro camera system, and Dynamic Island.",
        "imageUrl": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=300&h=300&fit=crop"
    },
    {
        "id": 2,
        "name": "Samsung Galaxy S23 Ultra",
        "price": 124999,
        "originalPrice": 134999,
        "discount": "7% OFF",
        "category": "Electronics",
        "brand": "Samsung",
        "rating": 4.5,
        "reviews": 12850,
        "badge": "Editor's Choice",
        "description": "Premium Android flagship with S Pen, 200MP camera, and powerful performance.",
        "imageUrl": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=300&h=300&fit=crop"
    },
    {
        "id": 3,
        "name": "Sony WH-1000XM4 Headphones",
        "price": 29990,
        "originalPrice": 34990,
        "discount": "14% OFF",
        "category": "Electronics",
        "brand": "Sony",
        "rating": 4.7,
        "reviews": 8950,
        "badge": "Premium Quality",
        "description": "Industry-leading noise canceling wireless headphones with exceptional sound quality.",
        "imageUrl": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=300&h=300&fit=crop"
    },
    {
        "id": 11,
        "name": "MacBook Air M2",
        "price": 114900,
        "originalPrice": 119900,
        "discount": "4% OFF",
        "category": "Electronics",
        "brand": "Apple",
        "rating": 4.8,
        "reviews": 9340,
        "badge": "New Launch",
        "description": "Ultra-thin laptop powered by M2 chip with all-day battery life and stunning display.",
        "imageUrl": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=300&h=300&fit=crop"
    },
    {
        "id": 12,
        "name": "Dell XPS 13 Laptop",
        "price": 89999,
        "originalPrice": 99999,
        "discount": "10% OFF",
        "category": "Electronics",
        "brand": "Dell",
        "rating": 4.4,
        "reviews": 6780,
        "badge": "Business Choice",
        "description": "Premium ultrabook with Intel Core i7, 16GB RAM, and InfinityEdge display.",
        "imageUrl": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300&h=300&fit=crop"
    },
    {
        "id": 13,
        "name": "iPad Pro 11-inch",
        "price": 81900,
        "originalPrice": 89900,
        "discount": "9% OFF",
        "category": "Electronics",
        "brand": "Apple",
        "rating": 4.6,
        "reviews": 7890,
        "badge": "Creative Pro",
        "description": "Powerful tablet with M2 chip, perfect for creative work and productivity.",
        "imageUrl": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=300&h=300&fit=crop"
    },

    # Fashion Category (6 items)
    {
        "id": 4,
        "name": "Levi's Men's Slim Fit Jeans",
        "price": 2999,
        "originalPrice": 3999,
        "discount": "25% OFF",
        "category": "Fashion",
        "brand": "Levi's",
        "rating": 4.3,
        "reviews": 5640,
        "badge": "Trending",
        "description": "Classic slim fit jeans made from premium denim with modern styling.",
        "imageUrl": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=300&h=300&fit=crop"
    },
    {
        "id": 5,
        "name": "Nike Air Max 270",
        "price": 12995,
        "originalPrice": 14995,
        "discount": "13% OFF",
        "category": "Fashion",
        "brand": "Nike",
        "rating": 4.4,
        "reviews": 7250,
        "badge": "Popular",
        "description": "Comfortable running shoes with Max Air unit for exceptional cushioning.",
        "imageUrl": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop"
    },
    {
        "id": 10,
        "name": "H&M Cotton T-Shirt",
        "price": 799,
        "originalPrice": 999,
        "discount": "20% OFF",
        "category": "Fashion",
        "brand": "H&M",
        "rating": 4.2,
        "reviews": 4320,
        "badge": "Everyday Essential",
        "description": "Comfortable 100% cotton t-shirt in various colors and sizes.",
        "imageUrl": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=300&h=300&fit=crop"
    },
    {
        "id": 14,
        "name": "Adidas Ultraboost 22",
        "price": 16999,
        "originalPrice": 18999,
        "discount": "11% OFF",
        "category": "Fashion",
        "brand": "Adidas",
        "rating": 4.5,
        "reviews": 8920,
        "badge": "Running Elite",
        "description": "Premium running shoes with BOOST midsole and Primeknit upper for ultimate comfort.",
        "imageUrl": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=300&h=300&fit=crop"
    },
    {
        "id": 15,
        "name": "Zara Women's Blazer",
        "price": 4999,
        "originalPrice": 6999,
        "discount": "29% OFF",
        "category": "Fashion",
        "brand": "Zara",
        "rating": 4.3,
        "reviews": 3450,
        "badge": "Office Wear",
        "description": "Professional tailored blazer perfect for business meetings and formal occasions.",
        "imageUrl": "https://images.unsplash.com/photo-1594633312681-425c7b977ccd1?w=300&h=300&fit=crop"
    },
    {
        "id": 16,
        "name": "Ray-Ban Aviator Sunglasses",
        "price": 8999,
        "originalPrice": 11999,
        "discount": "25% OFF",
        "category": "Fashion",
        "brand": "Ray-Ban",
        "rating": 4.6,
        "reviews": 12340,
        "badge": "Classic Style",
        "description": "Iconic aviator sunglasses with premium lenses and timeless design.",
        "imageUrl": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=300&h=300&fit=crop"
    },

    # Home & Kitchen Category (6 items)
    {
        "id": 6,
        "name": "Instant Pot Duo 7-in-1",
        "price": 8999,
        "originalPrice": 12999,
        "discount": "31% OFF",
        "category": "Home & Kitchen",
        "brand": "Instant Pot",
        "rating": 4.6,
        "reviews": 3420,
        "badge": "Great Value",
        "description": "Multi-functional electric pressure cooker that replaces 7 kitchen appliances.",
        "imageUrl": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=300&h=300&fit=crop"
    },
    {
        "id": 8,
        "name": "Philips Air Fryer HD9200",
        "price": 12999,
        "originalPrice": 15999,
        "discount": "19% OFF",
        "category": "Home & Kitchen",
        "brand": "Philips",
        "rating": 4.5,
        "reviews": 2890,
        "badge": "Healthy Choice",
        "description": "Cook healthier meals with up to 90% less fat using rapid air technology.",
        "imageUrl": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=300&h=300&fit=crop"
    },
    {
        "id": 17,
        "name": "KitchenAid Stand Mixer",
        "price": 34999,
        "originalPrice": 39999,
        "discount": "13% OFF",
        "category": "Home & Kitchen",
        "brand": "KitchenAid",
        "rating": 4.7,
        "reviews": 1890,
        "badge": "Professional",
        "description": "Heavy-duty stand mixer perfect for baking and food preparation with multiple attachments.",
        "imageUrl": "https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=300&h=300&fit=crop"
    },
    {
        "id": 18,
        "name": "Dyson V15 Detect Vacuum",
        "price": 45999,
        "originalPrice": 52999,
        "discount": "13% OFF",
        "category": "Home & Kitchen",
        "brand": "Dyson",
        "rating": 4.8,
        "reviews": 4560,
        "badge": "Latest Tech",
        "description": "Cordless vacuum with laser dust detection and powerful suction technology.",
        "imageUrl": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop"
    },
    {
        "id": 19,
        "name": "Nespresso Coffee Machine",
        "price": 18999,
        "originalPrice": 22999,
        "discount": "17% OFF",
        "category": "Home & Kitchen",
        "brand": "Nespresso",
        "rating": 4.4,
        "reviews": 6780,
        "badge": "Barista Quality",
        "description": "Premium espresso machine with milk frother for café-quality coffee at home.",
        "imageUrl": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=300&h=300&fit=crop"
    },
    {
        "id": 20,
        "name": "IKEA Bookshelf BILLY",
        "price": 3999,
        "originalPrice": 4999,
        "discount": "20% OFF",
        "category": "Home & Kitchen",
        "brand": "IKEA",
        "rating": 4.2,
        "reviews": 8920,
        "badge": "Space Saver",
        "description": "Adjustable bookshelf perfect for organizing books and displaying decor items.",
        "imageUrl": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=300&h=300&fit=crop"
    },

    # Books Category (6 items)
    {
        "id": 7,
        "name": "The Alchemist by Paulo Coelho",
        "price": 299,
        "originalPrice": 399,
        "discount": "25% OFF",
        "category": "Books",
        "brand": "HarperCollins",
        "rating": 4.8,
        "reviews": 18950,
        "badge": "Bestseller",
        "description": "International bestseller about following your dreams and finding your destiny.",
        "imageUrl": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=300&h=300&fit=crop"
    },
    {
        "id": 9,
        "name": "Atomic Habits by James Clear",
        "price": 399,
        "originalPrice": 599,
        "discount": "33% OFF",
        "category": "Books",
        "brand": "Random House",
        "rating": 4.7,
        "reviews": 12450,
        "badge": "Life Changing",
        "description": "Proven strategies to build good habits and break bad ones.",
        "imageUrl": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=300&h=300&fit=crop"
    },
    {
        "id": 21,
        "name": "Think and Grow Rich",
        "price": 199,
        "originalPrice": 299,
        "discount": "33% OFF",
        "category": "Books",
        "brand": "Penguin Books",
        "rating": 4.6,
        "reviews": 24560,
        "badge": "Classic",
        "description": "Napoleon Hill's timeless guide to personal success and wealth building.",
        "imageUrl": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=300&h=300&fit=crop"
    },
    {
        "id": 22,
        "name": "Sapiens by Yuval Noah Harari",
        "price": 449,
        "originalPrice": 599,
        "discount": "25% OFF",
        "category": "Books",
        "brand": "Vintage Books",
        "rating": 4.5,
        "reviews": 16780,
        "badge": "Mind Expanding",
        "description": "A brief history of humankind exploring how Homo sapiens conquered the world.",
        "imageUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=300&fit=crop"
    },
    {
        "id": 23,
        "name": "The Power of Now by Eckhart Tolle",
        "price": 349,
        "originalPrice": 449,
        "discount": "22% OFF",
        "category": "Books",
        "brand": "New World Library",
        "rating": 4.4,
        "reviews": 11230,
        "badge": "Spiritual Guide",
        "description": "A guide to spiritual enlightenment and living in the present moment.",
        "imageUrl": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=300&h=300&fit=crop"
    },
    {
        "id": 24,
        "name": "Harry Potter Complete Series",
        "price": 2999,
        "originalPrice": 3999,
        "discount": "25% OFF",
        "category": "Books",
        "brand": "Bloomsbury",
        "rating": 4.9,
        "reviews": 45620,
        "badge": "Magic Collection",
        "description": "Complete 7-book set of J.K. Rowling's magical Harry Potter series.",
        "imageUrl": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=300&h=300&fit=crop"
    }
]

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('static', 'index.html')

@app.route('/products', methods=['GET'])
def get_products():
    """Get all available products"""
    return jsonify(PRODUCTS)

@app.route('/checkout', methods=['POST'])
def checkout():
    """Process checkout with cart items"""
    data = request.get_json(silent=True)

    if not data or 'items' not in data:
        return jsonify({"detail": "Invalid request data"}), 400

    items = data['items']

    if not items:
        return jsonify({"detail": "Cart is empty"}), 400

    # Calculate total and log order details
    total = 0.0
    order_details = []

    for item in items:
        # Validate item structure
        if 'productId' not in item or 'quantity' not in item:
            return jsonify({"detail": "Invalid item format"}), 400

        product_id = item['productId']
        quantity = item['quantity']

        # Find product
        product = next((p for p in PRODUCTS if p['id'] == product_id), None)
        if not product:
            return jsonify({"detail": f"Product with ID {product_id} not found"}), 400

        if quantity <= 0:
            return jsonify({"detail": "Quantity must be greater than 0"}), 400

        item_total = product['price'] * quantity
        total += item_total

        order_details.append({
            "product_name": product['name'],
            "price": product['price'],
            "quantity": quantity,
            "item_total": item_total
        })

    # Generate order ID
    order_id = str(uuid.uuid4())[:8].upper()

    # Log order to console
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'='*50}")
    print(f"NEW ORDER RECEIVED - {timestamp}")
    print(f"Order ID: {order_id}")
    print(f"{'='*50}")
    for detail in order_details:
        print(f"Product: {detail['product_name']}")
        print(f"Price: ₹{detail['price']:.2f}")
        print(f"Quantity: {detail['quantity']}")
        print(f"Item Total: ₹{detail['item_total']:.2f}")
        print("-" * 30)
    print(f"TOTAL AMOUNT: ₹{total:.2f}")
    print(f"{'='*50}\n")

    return jsonify({
        "success": True,
        "message": f"Order placed successfully! Your order ID is {order_id}",
        "orderId": order_id
    })

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"detail": getattr(error, "description", "Bad Request")}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"detail": "Not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"detail": "Method Not Allowed"}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"detail": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)