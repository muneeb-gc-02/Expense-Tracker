# Flask Expense Tracker

A modern, user-friendly web application for tracking personal expenses. This project was developed as a Final Year Project for the BSCS program, demonstrating proficiency in full-stack web development using the Flask framework. It allows users to register, log their daily expenses, categorize them, and export reports, all through a clean and responsive interface.

---

## Features

-   **User Authentication**: Secure user registration and login system with password hashing. Each user's data is private.
-   **Expense Management (CRUD)**: Users can Create, Read, Update, and Delete their expenses.
-   **Category Management**: Users can create and delete their own custom spending categories (e.g., Food, Transport, Bills).
-   **Dashboard Overview**: The main page displays a list of all expenses and calculates the total expenditure for a quick overview of spending habits.
-   **User Profile**: Users can set their preferred currency (PKR, USD, EUR, GBP), which is then reflected across the application.
-   **PDF Export**: Generate and download a professional PDF report of all expenses, complete with a title, export date, and clean table formatting.
-   **Modern & Responsive UI**: Built with Bootstrap 5 and custom CSS for a visually appealing and mobile-friendly experience on any device.
-   **Date Picker**: An intuitive date picker for easily selecting the date of an expense.

---

## Technology Stack

| Category      | Technology                                                                                                    |
| ------------- | ------------------------------------------------------------------------------------------------------------- |
| **Backend**   | [Flask](https://flask.palletsprojects.com/), [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/), [Flask-Login](https://flask-login.readthedocs.io/en/latest/) |
| **Database**  | [SQLite](https://www.sqlite.org/index.html)                                                                   |
| **Frontend**  | HTML5, CSS3, [Bootstrap 5](https://getbootstrap.com/), [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript), [jQuery](https://jquery.com/) |
| **Templating**| [Jinja2](https://jinja.palletsprojects.com/)                                                                  |
| **PDF Lib**   | [ReportLab](https://www.reportlab.com/)                                                                       |
| **Language**  | [Python 3](https://www.python.org/)                                                                           |

---

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

-   Python 3.9 or higher
-   pip (Python package installer)

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Create and activate a virtual environment:**
    *   On Windows:
        ```sh
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```sh
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install the required packages:**
    Create a file named `requirements.txt` and add the following lines:
    ```
    Flask
    Flask-Login
    Flask-SQLAlchemy
    Werkzeug
    reportlab
    ```
    Then, run the installation command:
    ```sh
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```sh
    python app.py
    ```
    The application will start in debug mode. The database file `expenses.db` will be automatically created in the project directory on the first run.

5.  **Access the application:**
    Open your web browser and navigate to `http://127.0.0.1:5000`.

---

## Usage Guide

1.  **Register:** Create a new account by providing a unique username, a password, and selecting your default currency.
2.  **Login:** Use your credentials to log in to your account.
3.  **Manage Categories:** Navigate to the "Categories" page to add or delete spending categories. Default categories are created upon registration.
4.  **Add Expense:** Go to the "Add Expense" page, fill in the amount, select a category, add an optional description, and pick the date.
5.  **View & Edit:** The "Home" page lists all your expenses. You can edit or delete any expense from here.
6.  **Export PDF:** Click the "Export PDF" link in the navigation bar to download a report of your expenses.
7.  **Update Profile:** Go to "Profile" to change your currency at any time.

---

## Project Structure

```
.
├── app.py                  # Main Flask application file (routes, logic, db models)
├── templates/
│   ├── base.html           # Base template with navbar and layout
│   ├── index.html          # Dashboard to display all expenses
│   ├── add_expense.html    # Form to add a new expense
│   ├── edit_expense.html   # Form to edit an existing expense
│   ├── categories.html     # Page to manage categories
│   ├── login.html          # User login page
│   ├── register.html       # User registration page
│   └── profile.html        # User profile page for currency settings
├── static/
│   ├── favicon-16x16.png   # Favicon files
│   ├── favicon-32x32.png
│   └── favicon-96x96.png
├── expenses.db             # SQLite database file (created on run)
└── README.md               # This file
```

---

## 💡 Future Enhancements

-   **Data Visualization**: Implement charts and graphs (e.g., using Chart.js) to visualize spending by category or over time.
-   **Advanced Reporting**: Add filtering options to the dashboard and PDF export (e.g., by date range, by category).
-   **Password Reset**: Implement a "Forgot Password" feature using email.
-   **Dockerization**: Containerize the application with Docker for easier deployment.
-   **API Endpoints**: Develop a RESTful API to allow for integration with a potential mobile application.
