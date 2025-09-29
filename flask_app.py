from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import datetime
import uuid

app = Flask(__name__, static_folder='static')

# Enable CORS for frontend communication
CORS(app)

# Realistic Indian e-commerce product data with authentic pricing and categories
PRODUCTS = [
    {
        "id": 1,
        "name": "boAt Rockerz 550 Wireless Bluetooth Headphones",
        "price": 2499,
        "originalPrice": 4990,
        "discount": "50% off",
        "category": "Electronics",
        "brand": "boAt",
        "rating": 4.2,
        "reviews": 47892,
        "badge": "Bestseller",
        "description": "Premium wireless headphones with 50mm drivers, 20 hours playback, and fast charging",
        "imageUrl": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop&auto=format"
    },
    {
        "id": 2,
        "name": "Redmi Note 12 Pro 5G (Glacier Blue, 128GB)",
        "price": 23999,
        "originalPrice": 27999,
        "discount": "14% off",
        "category": "Electronics",
        "brand": "Xiaomi",
        "rating": 4.4,
        "reviews": 28340,
        "badge": "Top Rated",
        "description": "50MP triple camera, MediaTek Dimensity 1080 processor, 67W turbo charging",
        "imageUrl": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop&auto=format"
    },
    {
        "id": 3,
        "name": "HP Pavilion 15 Gaming Laptop (Intel i5, 16GB RAM, 512GB SSD)",
        "price": 65999,
        "originalPrice": 79999,
        "discount": "17% off",
        "category": "Electronics",
        "brand": "HP",
        "rating": 4.3,
        "reviews": 12750,
        "badge": "Gaming",
        "description": "Intel Core i5-12450H, NVIDIA GTX 1650, 15.6\" FHD display, Windows 11",
        "imageUrl": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop&auto=format"
    },
    {
        "id": 4,
        "name": "Nestlé Everyday Premium Ceramic Coffee Mug Set (Set of 2)",
        "price": 399,
        "originalPrice": 799,
        "discount": "50% off",
        "category": "Home & Kitchen",
        "brand": "Nestlé",
        "rating": 4.1,
        "reviews": 8650,
        "badge": "Choice",
        "description": "Premium ceramic mugs with ergonomic handle, microwave & dishwasher safe",
        "imageUrl": "https://images.unsplash.com/photo-1514228742587-6b1558fcf93a?w=400&h=400&fit=crop&auto=format"
    },
    {
        "id": 5,
        "name": "Automate the Boring Stuff with Python - 2nd Edition",
        "price": 699,
        "originalPrice": 999,
        "discount": "30% off",
        "category": "Books",
        "brand": "No Starch Press",
        "rating": 4.6,
        "reviews": 15630,
        "badge": "Educational",
        "description": "Learn Python programming with practical projects and automation tasks",
        "imageUrl": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=400&fit=crop&auto=format"
    },
    {
        "id": 6,
        "name": "Philips Smart LED Desk Lamp with Wireless Charging",
        "price": 3499,
        "originalPrice": 4999,
        "discount": "30% off",
        "category": "Home & Kitchen",
        "brand": "Philips",
        "rating": 4.5,
        "reviews": 6840,
        "badge": "Smart",
        "description": "Touch control, wireless phone charging base, adjustable brightness & color temperature",
        "imageUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&auto=format"
    },
    {
        "id": 7,
        "name": "Logitech MX Master 3S Wireless Mouse",
        "price": 6999,
        "originalPrice": 8995,
        "discount": "22% off",
        "category": "Electronics",
        "brand": "Logitech",
        "rating": 4.7,
        "reviews": 21450,
        "badge": "Pro",
        "description": "Ultra-precise scrolling, customizable buttons, works on any surface including glass",
        "imageUrl": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=400&fit=crop&auto=format"
    },
    {
        "id": 8,
        "name": "Milton Thermosteel Water Bottle 750ml (Blue)",
        "price": 449,
        "originalPrice": 699,
        "discount": "36% off",
        "category": "Home & Kitchen",
        "brand": "Milton",
        "rating": 4.3,
        "reviews": 34560,
        "badge": "Trending",
        "description": "Double wall vacuum insulation, keeps drinks hot/cold for 24 hours, BPA free",
        "imageUrl": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400&h=400&fit=crop&auto=format"
    },
    {
        "id": 9,
        "name": "Titan Raga Viva Women's Analog Watch (Rose Gold)",
        "price": 8995,
        "originalPrice": 12500,
        "discount": "28% off",
        "category": "Fashion",
        "brand": "Titan",
        "rating": 4.4,
        "reviews": 9870,
        "badge": "Luxury",
        "description": "Elegant rose gold finish, mother of pearl dial, water resistant up to 30m",
        "imageUrl": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop&auto=format"
    },
    {
        "id": 10,
        "name": "Levi's Men's 511 Slim Jeans (Dark Blue)",
        "price": 2299,
        "originalPrice": 3999,
        "discount": "42% off",
        "category": "Fashion",
        "brand": "Levi's",
        "rating": 4.2,
        "reviews": 18920,
        "badge": "Classic",
        "description": "Classic slim fit jeans, premium denim fabric, comfortable stretch, multiple sizes",
        "imageUrl": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop&auto=format"
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