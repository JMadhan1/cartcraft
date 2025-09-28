import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_products():
    """Test the /products endpoint returns proper product data"""
    response = client.get("/products")
    
    # Check status code
    assert response.status_code == 200
    
    # Check response is a list
    products = response.json()
    assert isinstance(products, list)
    
    # Check we have products
    assert len(products) > 0
    
    # Check each product has required fields
    for product in products:
        assert "id" in product
        assert "name" in product
        assert "price" in product
        assert "imageUrl" in product
        
        # Check data types
        assert isinstance(product["id"], int)
        assert isinstance(product["name"], str)
        assert isinstance(product["price"], (int, float))
        assert isinstance(product["imageUrl"], str)
        
        # Check values are not empty
        assert product["name"].strip()
        assert product["imageUrl"].strip()
        assert product["price"] > 0

def test_checkout_success():
    """Test successful checkout with valid cart items"""
    checkout_data = {
        "items": [
            {"productId": 1, "quantity": 2},
            {"productId": 2, "quantity": 1}
        ]
    }
    
    response = client.post("/checkout", json=checkout_data)
    
    # Check status code
    assert response.status_code == 200
    
    # Check response structure
    result = response.json()
    assert "success" in result
    assert "message" in result
    assert "orderId" in result
    
    # Check values
    assert result["success"] is True
    assert isinstance(result["message"], str)
    assert len(result["orderId"]) > 0

def test_checkout_empty_cart():
    """Test checkout with empty cart returns error"""
    checkout_data = {"items": []}
    
    response = client.post("/checkout", json=checkout_data)
    
    # Should return 400 Bad Request
    assert response.status_code == 400

def test_checkout_invalid_product():
    """Test checkout with invalid product ID returns error"""
    checkout_data = {
        "items": [
            {"productId": 999, "quantity": 1}  # Non-existent product
        ]
    }
    
    response = client.post("/checkout", json=checkout_data)
    
    # Should return 400 Bad Request
    assert response.status_code == 400

def test_checkout_invalid_quantity():
    """Test checkout with invalid quantity returns error"""
    checkout_data = {
        "items": [
            {"productId": 1, "quantity": 0}  # Invalid quantity
        ]
    }
    
    response = client.post("/checkout", json=checkout_data)
    
    # Should return 400 Bad Request
    assert response.status_code == 400

def test_products_have_expected_count():
    """Test that we have the expected number of products (5-10 as per requirements)"""
    response = client.get("/products")
    products = response.json()
    
    # Should have between 5-10 products as per requirements
    assert 5 <= len(products) <= 10

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])