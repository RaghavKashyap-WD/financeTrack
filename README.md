# financeTrack

A comprehensive personal finance management application built with Flask and Python. Track your expenses, manage categories, visualize spending patterns, and maintain complete control over your financial data.

## Features

✨ **Core Features:**
- 👤 **User Authentication** - Secure registration and login system with
- 💰 **Expense Tracking** - Add, edit, and delete expenses with detailed information
- 🏷️ **Category Management** - Create and manage custom expense categories
- 📊 **Data Visualization** - Interactive charts and graphs to visualize spending patterns
- 🔐 **Secure Database** - MySQL database with SQLAlchemy ORM for data persistence
- 📅 **Date-based Aggregation** - View expense summaries grouped by date

## Tech Stack

- **Backend:** Flask (Python)
- **Database:** MySQL with SQLAlchemy ORM
- **Frontend:** HTML, CSS, JavaScript
- **Visualization:** Matplotlib for data visualization
- **Environment:** Python dotenv for configuration management

## Project Structure

```
financeTrack/
├── app.py              # Main Flask application entry point
├── config.py           # Database configuration and environment variables
├── models.py           # SQLAlchemy database models (User, Category, Expense)
├── db.py               # Database instance initialization
├── schemas.py          # Request/response schemas
├── crud.py             # CRUD operations for database models
├── requirements.txt    # Python dependencies
├── create_db.py        # Database initialization script
├── graphs/             # Expense visualization and graph generation
└── templates/          # HTML templates for web interface
```

## Database Models

### User
- user_id (Primary Key)
- username (Unique)
- email
- Relationships: Many expenses, many categories

### Category
- name (Unique)
- user_id (Foreign Key)
- Relationships: Many expenses

### Expense
- expense_id (Primary Key)
- amount
- description
- category_id (Foreign Key)
- user_id (Foreign Key)
- date
- Relationships: Belongs to User and Category

## Installation

### Prerequisites
- Python 3.7+
- MySQL Server
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/RaghavKashyap-WD/financeTrack.git
   cd financeTrack
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database credentials**
   - Create a `.env` file in the project root
   - Add the following environment variables:
   ```
   DB_USER=your_mysql_username
   DB_PASS=your_mysql_password
   DB_HOST=localhost
   DB_NAME=financetrack_db
   DB_PORT=3306
   ```

5. **Create the database**
   ```bash
   python create_db.py
   ```

6. **Run the application**
   ```bash
   python app.py
   ```
   The application will be available at `http://localhost:5000`

## Dependencies

- **SQLAlchemy** - SQL toolkit and Object-Relational Mapping (ORM)
- **PyMySQL** - MySQL database driver
- **python-dotenv** - Environment variable management
- **matplotlib** - Data visualization and graphing

See `requirements.txt` for complete list of dependencies.

### Creating an Account
1. Navigate to the registration page
2. Enter username, email, and password
3. Click register to create your account

### Managing Expenses
1. **Add Expense:**
   - Click "Add Expense" button
   - Enter amount, description, and select category
   - Choose date and submit

2. **View Expenses:**
   - See all your expenses in a table format
   - Filter by category or date range

3. **Update Expense:**
   - Click edit button next to any expense
   - Modify details and save

4. **Delete Expense:**
   - Click delete button to remove an expense

### Managing Categories
1. Create custom expense categories
2. View all categories and their expense summaries
3. Edit or delete categories as needed

### Visualizing Data
1. Access the analytics/graphs section
2. View expense distribution by category
3. See spending trends over time
4. Download or export visualizations

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user

### Expenses
- `GET /api/expenses` - Get all user expenses
- `POST /api/expenses` - Create new expense
- `GET /api/expenses/<id>` - Get specific expense
- `PUT /api/expenses/<id>` - Update expense
- `DELETE /api/expenses/<id>` - Delete expense
- `GET /api/expenses/aggregates` - Get expense aggregates by date

### Categories
- `GET /api/categories` - Get all user categories
- `POST /api/categories` - Create new category
- `PUT /api/categories/<id>` - Update category
- `DELETE /api/categories/<id>` - Delete category

## Testing

Run the test suite:
```bash
python test.py
```

## Project Status

This is a Class 12 school project demonstrating full-stack web development concepts including:
- Backend development with Flask
- Database design and management
- User authentication and security
- Data visualization techniques
- RESTful API design

## Future Enhancements

- 📱 Mobile-responsive design improvements
- 🔔 Transaction notifications and alerts
- 📈 Advanced analytics and reporting
- 💾 Data export to CSV/PDF
- 🌙 Dark mode support
- 🔐 OAuth2 authentication
- 📊 Budget tracking and forecasting
- 💳 Multi-account support

## Contributing

This is a school project. For questions or suggestions, please open an issue on GitHub.

## License

This project is open source and available under the MIT License.

## Author

**Raghav Kashyap** - [@RaghavKashyap-WD](https://github.com/RaghavKashyap-WD)

Class 12 CBSE - Full Stack Web Development Project (2024-2025)

## Acknowledgments

- Flask framework documentation
- SQLAlchemy ORM tutorials
- MySQL database concepts
- Matplotlib visualization guides
- Python security best practices

---

**Made with ❤️ as a school project demonstrating web development fundamentals**
