# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**Fyn** is a Smart Budgeting Assistant designed to aid in financial literacy education. It's a Streamlit-based web application that integrates with the Capital One API (via Nessie sandbox) to provide personalized budgeting experiences with AI chatbot integration.

## Development Commands

### Running the Application
```bash
# Run the main application (landing page)
streamlit run landingPage.py

# Run the home page directly (bypasses landing page)
streamlit run home_page.py

# Run individual demos or components
python demo.py
python get_transactions.py
```

### Development Tools
```bash
# Check Python version
python --version

# Install dependencies (if requirements.txt exists)
pip install streamlit pandas plotly requests

# Debug with VS Code
# Use the existing .vscode/launch.json configuration for Python debugging
```

## Code Architecture

### Core Application Structure

**Multi-Page Streamlit App**: The application uses Streamlit's page navigation system with separate Python files for different views.

**Authentication Flow**: 
- `landingPage.py` → `home_page.py` (with login authentication)
- Hardcoded credentials in `USER_CREDENTIALS` dictionary
- Session state management for authentication persistence

**Data Pipeline**:
1. `get_transactions.py` - Capital One API integration via Nessie sandbox
2. Data processing and visualization in `home_page.py`
3. Transaction categorization based on description parsing

### Key Components

**landingPage.py**: Landing page with company branding and navigation
- Custom CSS styling via `styles_landing.css`
- Single "Get Started" button for navigation

**home_page.py**: Main dashboard application
- Combines landing, login, and authenticated dashboard views
- Transaction visualization using Plotly
- Session state authentication system
- Metric cards for budget overview

**get_transactions.py**: API integration module
- Fetches transaction data from Capital One Nessie API
- Supports multiple customer profiles (3 hardcoded customer IDs)
- Outputs API responses to `output.json` for debugging

**demo.py**: Transaction processing demonstration
- Shows data analysis workflow using pandas
- Category grouping and aggregation example

### Data Flow Architecture

1. **API Integration**: `get_transactions.py` connects to Nessie API using hardcoded API key
2. **Data Processing**: Transaction data is cleaned and categorized in `home_page.py`
3. **Visualization**: Plotly creates interactive charts for spending analysis
4. **State Management**: Streamlit session state handles user authentication and data persistence

### Authentication System

The app uses a simple hardcoded authentication system:
- Username/password pairs stored in `USER_CREDENTIALS`
- Session state tracks authentication status
- Login required to access main dashboard features

### API Configuration

- **API Provider**: Capital One Nessie (sandbox environment)
- **API Key**: Hardcoded in `get_transactions.py`
- **Customer IDs**: Three predefined customer profiles for demo purposes
- **Data Output**: API responses saved to `output.json` and `transactions.json`

### Styling System

- **Landing Page**: `styles_landing.css` - Enhanced glassmorphism with animated gradients and floating particles
- **Main App**: `styles.css` - Modern dashboard with React-like components and micro-interactions
- **Advanced Components**: `styles_advanced.css` - Reusable CSS components (modals, toasts, loading spinners, etc.)
- **Color Scheme**: Purple/pink gradient palette with glassmorphism effects
- **Animations**: Entrance animations, hover effects, and React-like transitions

## Important File Locations

- **Main Entry Points**: `landingPage.py`, `home_page.py`
- **API Integration**: `get_transactions.py`
- **Styling**: `styles_landing.css`, `styles.css`, `styles_advanced.css`
- **UI Demo**: `advanced_components_example.html` - Preview of enhanced components
- **Data Files**: `output.json`, `transactions.json`, `alice-mock-data.json`
- **Debug Configuration**: `.vscode/launch.json`

## Development Notes

### API Integration
- The application uses hardcoded API credentials for demo purposes
- Three customer profiles are available (IDs 0, 1, 2 in `fetch_trans()` function)
- API responses are cached in JSON files for debugging

### Data Processing
- Transaction descriptions are parsed to extract category information (first word)
- Date formatting and sorting is handled for chronological display
- Amount calculations handle both positive and negative transactions

### Streamlit Specifics
- Page navigation uses `st.switch_page()` for routing
- Session state is crucial for authentication flow
- CSS is loaded dynamically based on authentication state
- Plotly charts are integrated with `use_container_width=True` for responsive design