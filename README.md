# Hotel Kitchen Preparation Management System

## Overview
This system is designed to manage kitchen preparations, banquet events, and ingredient requirements for hotels and restaurants.

## Key Features
- Kitchen preparation task management
- Banquet event scheduling
- Ingredient requirement tracking
- Real-time kitchen status monitoring

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- PostgreSQL 12+
- MSSQL Server

### Backend Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\\venv\\Scripts\\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables
4. Run migrations
5. Start the server:
   ```bash
   python backend/app.py
   ```

### Frontend Setup
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the development server:
   ```bash
   npm start
   ```

## Project Structure
- `/backend` - Flask backend application
- `/frontend` - React frontend application
- `/docs` - Project documentation

## License
MIT License