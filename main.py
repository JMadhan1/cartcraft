from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import datetime
import uuid

app = FastAPI(title="Simple Shopping Cart API", version="1.0.0")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files for frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic models
class Product(BaseModel):
    id: int
    name: str
    price: float
    imageUrl: str

class CartItem(BaseModel):
    productId: int
    quantity: int

class CheckoutRequest(BaseModel):
    items: List[CartItem]

class CheckoutResponse(BaseModel):
    success: bool
    message: str
    orderId: str

# Hardcoded product data
PRODUCTS = [
    Product(
        id=1,
        name="Wireless Bluetooth Headphones",
        price=2499.99,
        imageUrl="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop"
    ),
    Product(
        id=2,
        name="Smartphone",
        price=15999.99,
        imageUrl="https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop"
    ),
    Product(
        id=3,
        name="Laptop Computer",
        price=45999.99,
        imageUrl="https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop"
    ),
    Product(
        id=4,
        name="Coffee Mug",
        price=299.99,
        imageUrl="https://images.unsplash.com/photo-1514228742587-6b1558fcf93a?w=400&h=400&fit=crop"
    ),
    Product(
        id=5,
        name="Book - Python Programming",
        price=599.99,
        imageUrl="https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=400&fit=crop"
    ),
    Product(
        id=6,
        name="Desk Lamp",
        price=1299.99,
        imageUrl="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop"
    ),
    Product(
        id=7,
        name="Wireless Mouse",
        price=899.99,
        imageUrl="https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=400&fit=crop"
    ),
    Product(
        id=8,
        name="Water Bottle",
        price=199.99,
        imageUrl="https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400&h=400&fit=crop"
    )
]

@app.get("/")
async def read_root():
    return FileResponse('static/index.html')

@app.get("/products", response_model=List[Product])
async def get_products():
    """Get all available products"""
    return PRODUCTS

@app.post("/checkout", response_model=CheckoutResponse)
async def checkout(request: CheckoutRequest):
    """Process checkout with cart items"""
    if not request.items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    # Calculate total and log order details
    total = 0.0
    order_details = []
    
    for item in request.items:
        # Find product
        product = next((p for p in PRODUCTS if p.id == item.productId), None)
        if not product:
            raise HTTPException(status_code=400, detail=f"Product with ID {item.productId} not found")
        
        if item.quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
        
        item_total = product.price * item.quantity
        total += item_total
        
        order_details.append({
            "product_name": product.name,
            "price": product.price,
            "quantity": item.quantity,
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
    
    return CheckoutResponse(
        success=True,
        message=f"Order placed successfully! Your order ID is {order_id}",
        orderId=order_id
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)