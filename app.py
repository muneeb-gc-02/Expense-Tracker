from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO
from flask import send_file

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Currency codes
CURRENCY_CODES = {
    'USD': 'USD',
    'EUR': 'EUR',
    'GBP': 'GBP',
    'PKR': 'PKR'
}

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    currency = db.Column(db.String(10), default='PKR')

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('expenses', lazy=True))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
@login_required
def index():
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()
    total = sum(expense.amount for expense in expenses)
    return render_template('index.html', expenses=expenses, total=total, currency=CURRENCY_CODES.get(current_user.currency, current_user.currency))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    categories = Category.query.filter_by(user_id=current_user.id).all()
    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            category_id = int(request.form['category'])
            description = request.form['description']
            date = datetime.strptime(request.form['date'], '%Y-%m-%d')
            
            expense = Expense(
                amount=amount,
                category_id=category_id,
                description=description,
                date=date,
                user_id=current_user.id
            )
            db.session.add(expense)
            db.session.commit()
            flash('Expense added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error adding expense: {str(e)}', 'danger')
    return render_template('add_expense.html', categories=categories, currency=CURRENCY_CODES.get(current_user.currency, current_user.currency))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_expense(id):
    expense = Expense.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    categories = Category.query.filter_by(user_id=current_user.id).all()
    if request.method == 'POST':
        try:
            expense.amount = float(request.form['amount'])
            expense.category_id = int(request.form['category'])
            expense.description = request.form['description']
            expense.date = datetime.strptime(request.form['date'], '%Y-%m-%d')
            db.session.commit()
            flash('Expense updated successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error updating expense: {str(e)}', 'danger')
    return render_template('edit_expense.html', expense=expense, categories=categories, currency=CURRENCY_CODES.get(current_user.currency, current_user.currency))

@app.route('/delete/<int:id>')
@login_required
def delete_expense(id):
    expense = Expense.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Clear any existing session to ensure user is logged out
    if current_user.is_authenticated:
        logout_user()
    session.clear()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        currency = request.form['currency']
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
        else:
            user = User(
                username=username,
                password_hash=generate_password_hash(password),
                currency=currency
            )
            db.session.add(user)
            db.session.commit()
            # Add default categories for the new user
            default_categories = ['Food', 'Transport', 'Entertainment', 'Bills', 'Other']
            for category_name in default_categories:
                category = Category(name=category_name, user_id=user.id)
                db.session.add(category)
            db.session.commit()
            flash('Registration successful! Please log in to continue.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))

@app.route('/categories', methods=['GET', 'POST'])
@login_required
def manage_categories():
    if request.method == 'POST':
        name = request.form['name']
        if Category.query.filter_by(name=name, user_id=current_user.id).first():
            flash('Category already exists!', 'danger')
        else:
            category = Category(name=name, user_id=current_user.id)
            db.session.add(category)
            db.session.commit()
            flash('Category added successfully!', 'success')
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('categories.html', categories=categories)

@app.route('/delete_category/<int:id>')
@login_required
def delete_category(id):
    category = Category.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    if Expense.query.filter_by(category_id=id, user_id=current_user.id).first():
        flash('Cannot delete category with associated expenses!', 'danger')
    else:
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted successfully!', 'success')
    return redirect(url_for('manage_categories'))

@app.route('/export_pdf')
@login_required
def export_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title and Export Date
    title = f"Expense Report for {current_user.username}"
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elements.append(Paragraph(f"<b>{title}</b>", styles['Heading1']))
    elements.append(Paragraph(f"Export Date: {date_str}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Table Data with Currency Codes
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()
    table_data = [['Date', 'Category', 'Description', 'Amount']]
    for expense in expenses:
        code = CURRENCY_CODES.get(current_user.currency, current_user.currency)
        table_data.append([
            expense.date.strftime('%Y-%m-%d'),
            expense.category.name,
            expense.description or 'N/A',
            f"{code} {expense.amount:.2f}"
        ])

    # Create Table with Modern Styling
    table = Table(table_data, colWidths=[1.5*inch, 1.5*inch, 2.5*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0077B6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.grey),
    ]))
    elements.append(table)

    # Add Page Number
    from reportlab.lib.utils import simpleSplit
    def add_page_number(canvas, doc):
        page_num = canvas.getPageNumber()
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(letter[0] - 50, 30, f"Page {page_num}")

    # Set PDF metadata title
    doc.title = title

    doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f'{title}.pdf', mimetype='application/pdf')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.currency = request.form['currency']
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    return render_template('profile.html', user=current_user)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)