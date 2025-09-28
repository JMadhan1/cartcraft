import pytest
import json
from flask_app import app

@pytest.fixture
def client():
    """Create test client for Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_products(client):
    """Test the /products endpoint returns proper product data"""
    response = client.get('/products')
    
    # Check status code
    assert response.status_code == 200
    
    # Check response is a list
    products = response.get_json()
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

def test_checkout_success(client):
    """Test successful checkout with valid cart items"""
    checkout_data = {
        "items": [
            {"productId": 1, "quantity": 2},
            {"productId": 2, "quantity": 1}
        ]
    }
    
    response = client.post('/checkout', 
                          data=json.dumps(checkout_data),
                          content_type='application/json')
    
    # Check status code
    assert response.status_code == 200
    
    # Check response structure
    result = response.get_json()
    assert "success" in result
    assert "message" in result
    assert "orderId" in result
    
    # Check values
    assert result["success"] is True
    assert isinstance(result["message"], str)
    assert len(result["orderId"]) > 0

def test_checkout_empty_cart(client):
    """Test checkout with empty cart returns error"""
    checkout_data = {"items": []}
    
    response = client.post('/checkout',
                          data=json.dumps(checkout_data),
                          content_type='application/json')
    
    # Should return 400 Bad Request
    assert response.status_code == 400

def test_checkout_invalid_product(client):
    """Test checkout with invalid product ID returns error"""
    checkout_data = {
        "items": [
            {"productId": 999, "quantity": 1}  # Non-existent product
        ]
    }
    
    response = client.post('/checkout',
                          data=json.dumps(checkout_data),
                          content_type='application/json')
    
    # Should return 400 Bad Request
    assert response.status_code == 400

def test_checkout_invalid_quantity(client):
    """Test checkout with invalid quantity returns error"""
    checkout_data = {
        "items": [
            {"productId": 1, "quantity": 0}  # Invalid quantity
        ]
    }
    
    response = client.post('/checkout',
                          data=json.dumps(checkout_data),
                          content_type='application/json')
    
    # Should return 400 Bad Request
    assert response.status_code == 400

def test_products_have_expected_count(client):
    """Test that we have the expected number of products (5-10 as per requirements)"""
    response = client.get('/products')
    products = response.get_json()
    
    # Should have between 5-10 products as per requirements
    assert 5 <= len(products) <= 10

def test_index_route(client):
    """Test that the index route serves the HTML file"""
    response = client.get('/')
    
    # Should return 200 OK
    assert response.status_code == 200
    
    # Should return HTML content
    assert 'text/html' in response.content_type

def test_checkout_missing_data(client):
    """Test checkout with missing request data"""
    response = client.post('/checkout',
                          data=json.dumps({}),
                          content_type='application/json')
    
    # Should return 400 Bad Request
    assert response.status_code == 400

def test_checkout_invalid_item_structure(client):
    """Test checkout with invalid item structure"""
    checkout_data = {
        "items": [
            {"wrongField": 1, "anotherWrongField": 2}  # Missing productId and quantity
        ]
    }
    
    response = client.post('/checkout',
                          data=json.dumps(checkout_data),
                          content_type='application/json')
    
    # Should return 400 Bad Request
    assert response.status_code == 400

def test_error_schema_consistency(client):
    """Test that all error responses use consistent {"detail": "..."} schema"""
    # Test 400 with empty cart
    response = client.post('/checkout',
                          data=json.dumps({"items": []}),
                          content_type='application/json')
    assert response.status_code == 400
    error_data = response.get_json()
    assert "detail" in error_data
    assert isinstance(error_data["detail"], str)
    
    # Test 400 with invalid product
    response = client.post('/checkout',
                          data=json.dumps({"items": [{"productId": 999, "quantity": 1}]}),
                          content_type='application/json')
    assert response.status_code == 400
    error_data = response.get_json()
    assert "detail" in error_data
    
    # Test 404
    response = client.get('/nonexistent-endpoint')
    assert response.status_code == 404
    error_data = response.get_json()
    assert "detail" in error_data
    
    # Test 405 (Method Not Allowed)
    response = client.post('/products')  # GET endpoint called with POST
    assert response.status_code == 405
    error_data = response.get_json()
    assert "detail" in error_data

def test_malformed_json_handling(client):
    """Test that malformed JSON is handled gracefully"""
    response = client.post('/checkout',
                          data='{"invalid": json}',  # Malformed JSON
                          content_type='application/json')
    
    # Should return 400 Bad Request with detail
    assert response.status_code == 400
    error_data = response.get_json()
    assert "detail" in error_data

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])