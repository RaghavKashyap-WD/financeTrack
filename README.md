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

117
## Usage

### CLI Interface Overview

When you run the application, you'll see the following menu interface:

```
===== Expense Tracker =====
Auth:
  r) Register
  l) Login
  o) Logout

Actions (login required):
1) Create category
2) Add expense
3) List my expenses
4) Update expense
5) Delete expense
6) Show expense graph
7) Exit

Choose option: █
```

### Step-by-Step Usage

**1. Register a New Account**
   - Press 'r' at the main menu
   - Enter desired username
   - Enter email address
   - Choose your password
   - Account created successfully

**2. Login to Your Account**
   - Press 'l' at the main menu
   - Enter username or email
   - Enter your password
   - Access user action menu

**3. Create a Category** (Option 1)
   - Select option '1' from actions menu
   - Enter category name (e.g., "Food", "Transport", "Entertainment")
   - Category saved to database

**4. Add an Expense** (Option 2)
   - Select option '2' from actions menu
   - Enter expense amount
   - Add description/notes
   - Select from existing categories or create new
   - Expense recorded with current date

**5. View All Your Expenses** (Option 3)
   - Select option '3' from actions menu
   - View table of all your expenses
   - Shows: Amount, Description, Category, Date
   - Filter or sort as needed

**6. Update an Expense** (Option 4)
   - Select option '4' from actions menu
   - Choose expense to modify
   - Update amount, description, or category
   - Changes saved to database

**7. Delete an Expense** (Option 5)
   - Select option '5' from actions menu
   - Select expense to remove
   - Confirm deletion
   - Expense permanently removed

**8. View Expense Graph** (Option 6)
   - Select option '6' from actions menu
   - Displays graph of expenses
   - Visual representation of spending by category
   - Shows spending trends

**9. Logout** (Option 'o')
   - Press 'o' to logout
   - Return to main authentication menu
   - Session ends

**10. Exit Application** (Option 7)
   - Select option '7' to exit
   - Closes the application

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

## Author

**Raghav Kashyap** - [@RaghavKashyap-WD](https://github.com/RaghavKashyap-WD)

Class 12 CBSE - Full Stack Python Project (2025-2026)

## Acknowledgments

- Python documentation
- SQLAlchemy ORM tutorials
- MySQL database concepts
- Matplotlib visualization guides
- Database design best practices

---

**Made with ❤️ as a school project demonstrating Python and database fundamentals**
