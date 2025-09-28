# Overview

CartCraft is a simple full-stack e-commerce shopping cart application built with FastAPI backend and vanilla HTML/CSS/JavaScript frontend. The application provides a minimal but polished shopping experience with product browsing, cart management, and checkout functionality. It demonstrates core e-commerce patterns including product catalog display, shopping cart state management, and order processing.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Vanilla JavaScript SPA**: Uses a class-based architecture with the `ShoppingCart` class managing all frontend state and interactions
- **Component-based UI**: Modular approach with separate concerns for product display, cart management, and checkout flow
- **Local Storage Integration**: Cart state persists across browser sessions using localStorage
- **Modal-based UX**: Cart and success notifications use overlay modals for better user experience
- **Responsive Design**: CSS Grid and Flexbox for mobile-friendly layouts

## Backend Architecture
- **FastAPI Framework**: RESTful API with automatic OpenAPI documentation and request validation
- **Pydantic Models**: Type-safe data validation for API requests and responses using `Product`, `CartItem`, `CheckoutRequest`, and `CheckoutResponse` models
- **Static File Serving**: Integrated static file serving for the frontend assets
- **CORS Enabled**: Cross-origin resource sharing configured for frontend-backend communication
- **Hardcoded Data**: Simple in-memory product catalog without external database dependencies

## API Design
- **GET /products**: Returns product catalog with id, name, price, and image URLs
- **POST /checkout**: Processes cart items and returns order confirmation
- **Static file serving**: Frontend assets served from `/static` route
- **Error Handling**: HTTP exceptions for invalid requests and server errors

## Data Management
- **Frontend State**: JavaScript class manages cart state with localStorage persistence
- **Backend Data**: Products stored as hardcoded Python objects, no database required
- **Order Processing**: Simple logging-based order handling with UUID generation for order IDs

# External Dependencies

## Backend Dependencies
- **FastAPI**: Web framework for building the REST API
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server for running the FastAPI application (implied)

## Frontend Dependencies
- **Fetch API**: Native browser API for HTTP requests to backend
- **Local Storage API**: Browser storage for cart persistence
- **Unsplash**: External image service for product photos via CDN URLs

## Development Dependencies
- **pytest**: Testing framework for backend API testing
- **TestClient**: FastAPI's testing utilities for HTTP request simulation

## Third-party Services
- **Unsplash Images**: Product images sourced from Unsplash CDN for placeholder content
- **No Payment Processing**: Checkout is simulation-only without real payment integration
- **No Database**: Application uses in-memory data storage only