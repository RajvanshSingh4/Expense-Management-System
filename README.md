# Expense Management System

A full-stack web application for tracking and analyzing personal expenses, built with FastAPI backend and Streamlit frontend.

## 🚀 Features

- **Add/Update Expenses**: Record daily expenses with categories, amounts, and notes
- **Date-Range Analytics**: View expense summaries and visualizations for custom date ranges
- **Monthly Analytics**: Track spending patterns across different months
- **Category Breakdown**: Analyze expenses by categories (Food, Entertainment, Shopping, Rent, Other)
- **Interactive Charts**: Visual representations of spending data with percentages

## 🏗️ Architecture

### Backend (FastAPI)
- RESTful API endpoints for expense management
- MySQL database integration
- Comprehensive logging system
- Data validation with Pydantic models

### Frontend (Streamlit)
- Interactive web interface with tabbed navigation
- Real-time data visualization
- Form-based expense entry
- Responsive charts and tables

### Database (MySQL)
- Structured expense storage
- Optimized queries for analytics
- Date-based expense tracking

## 📁 Project Structure

```
expense-manager/
├── backend/
│   ├── server.py           
│   ├── db_helper.py        
│   └── logging_setup.py    
├── frontend/
│   └── app.py             
├── database/
│   └── expense_db_creation.sql  
├── test/
│   ├── backend/
│   │   └── test_db_helper.py    
│   ├── frontend/
│   │   └── test_app.py          
│   └── conftest.py              
├── requirements.txt        
├── .gitignore             
└── README.md              
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL Server
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd expense-manager
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

**Note**: Consider using a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Database Setup
1. Install MySQL and create a database named `expense_manager`:
```sql
CREATE DATABASE expense_manager;
```
2. Run the SQL script to create the expenses table:
```bash
mysql -u your_username -p expense_manager < database/expense_db_creation.sql
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```env
# Database Configuration
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=expense_manager

# API Configuration
API_HOST=http://127.0.0.1:8000
```

### 5. Start the Backend Server
Open a terminal and run:
```bash
cd backend
uvicorn server:app --reload --host 127.0.0.1 --port 8000
```

### 6. Start the Frontend Application
Open a new terminal and run:
```bash
cd frontend
streamlit run app.py
```

The application will be available at `http://localhost:8501` (Streamlit default port).

## 🔌 API Endpoints

### Expenses
- `GET /expenses/{expense_date}` - Get expenses for a specific date
- `POST /expenses/{expense_date}` - Add/update expenses for a date

### Analytics
- `POST /analytics` - Get expense summary for a date range
- `GET /monthly/analytics` - Get monthly expense breakdown

### Example API Usage
```http
# GET EXPENSES FOR A SPECIFIC DATE
GET /expenses/2024-08-01



# ADD EXPENSES (body should be an array directly)
POST /expenses/2024-08-01
[
  {
    "amount": 50.0,
    "category": "Food",
    "notes": "Lunch at restaurant"
  }
]



# GET ANALYTICS FOR A DATE RANGE
POST /analytics
{
  "start_date": "2024-08-01",
  "end_date": "2024-08-31"
}
```

## 🧪 Testing

Run the test suite:
```bash
# Run all tests from project root
pytest

# Run specific test file
pytest test/backend/test_db_helper.py

# Run with verbose output
pytest -v
```

## 📊 Database Schema

### Expenses Table
| Column | Type | Description |
|--------|------|-------------|
| id | INT (PK, Auto-increment) | Unique expense ID |
| expense_date | DATE | Date of the expense |
| amount | FLOAT | Expense amount |
| category | VARCHAR(255) | Expense category |
| notes | TEXT | Additional notes |

## 🎯 Usage

1. **Adding Expenses**: Use the "Add/Update" tab to record daily expenses
2. **View Analytics**: Use "Analytics By Date" to see spending patterns for custom periods
3. **Monthly Overview**: Check "Analytics By Month" for month-wise expense breakdown

## 🔧 Configuration

### Categories
Default expense categories include:
- Food
- Entertainment  
- Shopping
- Rent
- Other

Categories can be modified in `frontend/app.py`.

### Logging
Logs are stored in `server.log` with configurable levels in `logging_setup.py`.



## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request



## 🐛 Known Issues

- Frontend tests need implementation
- Error handling could be enhanced for network failures
- Date validation on frontend could be improved


## 📧 Contact

If you like this project or have any questions, feel free to reach out!

- **Email**: [rajvanshsingh4@gmail.com](mailto:rajvanshsingh4@gmail.com)
- **LinkedIn**: [https://www.linkedin.com/in/rajvansh-singh/](https://www.linkedin.com/in/rajvansh-singh/)

---

**Happy Expense Tracking! 💰**