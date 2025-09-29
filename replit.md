# Overview

CartCraft is a premium full-stack e-commerce shopping cart application built with Flask backend and modern vanilla HTML/CSS/JavaScript frontend. The application provides a professional and visually stunning shopping experience with comprehensive e-commerce functionality including product browsing, advanced search and filtering, wishlist management, cart functionality, and checkout processing. It demonstrates modern web development patterns with Indian market focus, responsive design, dark mode support, and micro-interactions that create an outstanding user experience.

# User Preferences

Preferred communication style: Simple, everyday language.

# Recent Changes (September 2025)

## Major Enhancement Update
- **Complete Visual Redesign**: Transformed from basic shopping cart to premium e-commerce platform
- **Indian Market Focus**: Added 10 realistic products with authentic Indian brands and pricing
- **Advanced Features**: Search, filtering, wishlist, dark mode, quick view, and enhanced cart functionality
- **Modern UI/UX**: Gradient designs, smooth animations, micro-interactions, and professional styling
- **Enhanced Accessibility**: Keyboard navigation, focus management, and semantic HTML improvements

## New Features Added
1. **Smart Search & Filtering**: Real-time product search with category filtering
2. **Wishlist Management**: Heart icons, separate wishlist view, and batch cart addition
3. **Dark Mode Toggle**: Smooth theme transitions with user preference persistence
4. **Product Quick View**: Modal with enlarged images and detailed product information
5. **Enhanced Cart Experience**: Order summary with tax calculation, promo code support, and detailed item management
6. **Toast Notification System**: Real-time feedback for user actions with professional styling
7. **Responsive Design**: Mobile-first approach with optimized layouts for all screen sizes
8. **Keyboard Shortcuts**: Power user features for faster navigation (/, c, w, t, Escape)

# System Architecture

## Frontend Architecture
- **Modern Vanilla JavaScript SPA**: Uses a class-based architecture with the `CartCraft` class managing all frontend state, interactions, and advanced features
- **Component-based UI**: Modular approach with separate concerns for product display, search/filtering, wishlist management, cart functionality, and checkout flow
- **Advanced State Management**: Multiple localStorage integrations for cart, wishlist, and theme persistence across browser sessions
- **Professional Modal System**: Enhanced modals for cart, wishlist, quick view, and success notifications with smooth animations
- **Responsive & Accessible Design**: CSS Grid and Flexbox with mobile-first approach, keyboard navigation, and focus management
- **Modern UI/UX Features**: Dark mode support, search functionality, product filtering, toast notifications, micro-interactions, and loading states

## Backend Architecture
- **Flask Framework**: Lightweight REST API with comprehensive error handling and JSON response formatting
- **Enhanced Product Data**: Realistic Indian e-commerce products with authentic pricing, categories, brands, ratings, and reviews
- **Comprehensive Error Handling**: Consistent JSON error responses with detailed validation messages
- **Static File Serving**: Optimized static file serving for frontend assets with proper caching headers
- **CORS Enabled**: Cross-origin resource sharing configured for seamless frontend-backend communication
- **Rich Product Schema**: In-memory product catalog with extended metadata including discounts, badges, descriptions, and ratings

## API Design
- **GET /products**: Returns comprehensive product catalog with id, name, price, originalPrice, discount, category, brand, rating, reviews, badge, description, and optimized image URLs
- **POST /checkout**: Advanced checkout processing with cart validation, order logging, and structured confirmation responses
- **Static file serving**: Optimized frontend assets served from `/static` route with proper content types
- **Comprehensive Error Handling**: Unified JSON error responses for 400, 404, 405, and 500 status codes with detailed messages

## Data Management
- **Advanced Frontend State**: Multi-layered state management for cart, wishlist, theme preferences, and search filters with localStorage persistence
- **Rich Product Data**: 10 realistic Indian e-commerce products with authentic brands (boAt, Xiaomi, HP, Nestlé, Philips, Logitech, Milton, Titan, Levi's) and market-relevant pricing
- **Enhanced Order Processing**: Detailed order logging with itemized breakdowns, tax calculations, and unique order ID generation

# External Dependencies

## Backend Dependencies
- **Flask**: Lightweight web framework for building the REST API
- **Flask-CORS**: Cross-origin resource sharing support for frontend communication
- **Python Standard Library**: UUID generation, datetime handling, and JSON processing

## Frontend Dependencies
- **Fetch API**: Native browser API for HTTP requests to backend
- **Local Storage API**: Browser storage for cart, wishlist, and theme persistence
- **Google Fonts**: Inter font family for modern typography
- **Font Awesome**: Comprehensive icon library for UI elements and micro-interactions
- **Unsplash**: High-quality product images via optimized CDN URLs with auto-formatting

## Development Dependencies
- **pytest**: Comprehensive testing framework for backend API testing with 11 test cases
- **Flask Test Client**: Flask's built-in testing utilities for HTTP request simulation and response validation

## Third-party Services
- **Unsplash Images**: Professional product photography sourced from Unsplash CDN with responsive image optimization
- **Google Fonts CDN**: Web font delivery for consistent typography across devices
- **Font Awesome CDN**: Icon font delivery for consistent iconography
- **No Payment Processing**: Secure checkout simulation with order confirmation (ready for payment gateway integration)
- **No Database**: Optimized in-memory data storage with rich product metadata