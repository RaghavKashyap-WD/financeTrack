# financeTrack

A command-line personal finance management application built with Python. Track your expenses, manage categories, and visualize spending patterns through an interactive CLI interface.

## Features

✨ **Core Features:**
- 👤 **User Authentication** - User registration and login system
- 💰 **Expense Tracking** - Add, view, update, and delete expenses through CLI
- 🏷️ **Category Management** - Create and manage custom expense categories
- 📊 **Data Visualization** - Generate graphs to visualize spending patterns
- 🔐 **Data Persistence** - MySQL database with SQLAlchemy ORM
- 📅 **Expense Filtering** - View expenses by category, date, or user

## Tech Stack

- **Backend:** Python with CLI interface
- **Database:** MySQL with SQLAlchemy ORM
- **Visualization:** Matplotlib for charts and graphs
- **Environment:** Python dotenv for configuration management

## Project Structure

```
financeTrack/
├── app.py              # Main CLI application entry point
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
- category_id (Primary Key)
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

## Dependencies

- **SQLAlchemy** - SQL toolkit and Object-Relational Mapping (ORM)
- **PyMySQL** - MySQL database driver
- **python-dotenv** - Environment variable management
- **matplotlib** - Data visualization and graphing

See `requirements.txt` for complete list of dependencies.

## Usage

### Main Menu
When you run the application, you'll see a main menu with the following options:
```
1. Register
2. Login
3. Exit
```

### User Registration
1. Select "Register" from main menu
2. Enter desired username and email
3. Create a password
4. Account will be created successfully

### User Login
1. Select "Login" from main menu
2. Enter username or email
3. Enter password
4. On successful login, access user menu

### User Menu (After Login)
Once logged in, you have access to:

**1. Add Expense**
   - Enter expense amount
   - Add description
   - Select category (or create new one)
   - Save to database

**2. View All Expenses**
   - Display all expenses for current user
   - Shows amount, description, category, and date
   - Paginated or filtered view

**3. Update Expense**
   - Select expense from list
   - Modify amount, description, or category
   - Save changes

**4. Delete Expense**
   - Select expense to delete
   - Confirm deletion
   - Expense removed from database

**5. Manage Categories**
   - Create new expense categories
   - View all categories
   - Edit or delete categories

**6. View Charts/Visualizations**
   - Generate spending charts
   - View expense distribution by category
   - See spending trends

**7. Logout**
   - Return to main menu
   - Session ends

## Project Status

This is a Class 12 school project demonstrating:
- Python programming fundamentals
- Database design and management
- User authentication and session management
- CLI application development
- Data visualization techniques
- CRUD operations

## Future Enhancements

- 📊 Advanced analytics and reporting
- 💾 Data export to CSV/PDF
- 🔔 Budget tracking and alerts
- 📱 Web-based interface
- 💳 Multi-account support
- 🔐 Enhanced security features
- 📈 Recurring expense support
- 🎯 Budget goals and targets

## Contributing

This is a school project. For questions or suggestions, please open an issue on GitHub.

## License

This project is open source and available under the MIT License.

## Author

**Raghav Kashyap** - [@RaghavKashyap-WD](https://github.com/RaghavKashyap-WD)

Class 12 CBSE - Full Stack Python Project (2024-2025)

## Acknowledgments

- Python documentation
- SQLAlchemy ORM tutorials
- MySQL database concepts
- Matplotlib visualization guides
- Database design best practices

---

**Made with ❤️ as a school project demonstrating Python and database fundamentals**
