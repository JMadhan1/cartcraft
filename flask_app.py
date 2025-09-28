from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import datetime
import uuid

app = Flask(__name__, static_folder='static')

# Enable CORS for frontend communication
CORS(app)

# Product data structure (same as FastAPI version)
PRODUCTS = [
    {
        "id": 1,
        "name": "Wireless Bluetooth Headphones",
        "price": 2499.99,
        "imageUrl": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop"
    },
    {
        "id": 2,
        "name": "Smartphone",
        "price": 15999.99,
        "imageUrl": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop"
    },
    {
        "id": 3,
        "name": "Laptop Computer",
        "price": 45999.99,
        "imageUrl": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop"
    },
    {
        "id": 4,
        "name": "Coffee Mug",
        "price": 299.99,
        "imageUrl": "https://images.unsplash.com/photo-1514228742587-6b1558fcf93a?w=400&h=400&fit=crop"
    },
    {
        "id": 5,
        "name": "Book - Python Programming",
        "price": 599.99,
        "imageUrl": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=400&fit=crop"
    },
    {
        "id": 6,
        "name": "Desk Lamp",
        "price": 1299.99,
        "imageUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop"
    },
    {
        "id": 7,
        "name": "Wireless Mouse",
        "price": 899.99,
        "imageUrl": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=400&fit=crop"
    },
    {
        "id": 8,
        "name": "Water Bottle",
        "price": 199.99,
        "imageUrl": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400&h=400&fit=crop"
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
    data = request.get_json()
    
    if not data or 'items' not in data:
        return jsonify({"error": "Invalid request data"}), 400
    
    items = data['items']
    
    if not items:
        return jsonify({"error": "Cart is empty"}), 400
    
    # Calculate total and log order details
    total = 0.0
    order_details = []
    
    for item in items:
        # Validate item structure
        if 'productId' not in item or 'quantity' not in item:
            return jsonify({"error": "Invalid item format"}), 400
        
        product_id = item['productId']
        quantity = item['quantity']
        
        # Find product
        product = next((p for p in PRODUCTS if p['id'] == product_id), None)
        if not product:
            return jsonify({"error": f"Product with ID {product_id} not found"}), 400
        
        if quantity <= 0:
            return jsonify({"error": "Quantity must be greater than 0"}), 400
        
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

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)