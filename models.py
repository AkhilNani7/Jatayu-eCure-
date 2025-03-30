from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    address = db.Column(db.String(200))
    date_of_birth = db.Column(db.Date)
    is_admin = db.Column(db.Boolean, default=False)
    cart_items = db.relationship('CartItem', backref='user', lazy=True, cascade="all, delete-orphan")
    appointments = db.relationship('Appointment', backref='user', lazy=True, cascade="all, delete-orphan")
    prescriptions = db.relationship('Prescription', backref='user', lazy=True, cascade="all, delete-orphan")
    orders = db.relationship('Order', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15))
    specialty = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(200))
    experience_years = db.Column(db.Integer)
    bio = db.Column(db.Text)
    consultation_fee = db.Column(db.Float)
    available_days = db.Column(db.String(100)) # Comma separated days of week
    available_times = db.Column(db.String(200)) # JSON string of time slots
    appointments = db.relationship('Appointment', backref='doctor', lazy=True, cascade="all, delete-orphan")
    prescriptions = db.relationship('Prescription', backref='doctor', lazy=True, cascade="all, delete-orphan")


class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    generic_name = db.Column(db.String(100))
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    dosage = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    manufacturer = db.Column(db.String(100))
    requires_prescription = db.Column(db.Boolean, default=False)
    side_effects = db.Column(db.Text)
    cart_items = db.relationship('CartItem', backref='medicine', lazy=True, cascade="all, delete-orphan")
    order_items = db.relationship('OrderItem', backref='medicine', lazy=True, cascade="all, delete-orphan")


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.String(10), nullable=False)  # Format: HH:MM AM/PM
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    is_virtual = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_prescribed = db.Column(db.Date, default=datetime.utcnow().date())
    valid_until = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')  # active, filled, expired


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Float, nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, processing, shipped, delivered
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # Price at the time of order
    
class InsuranceApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    policy_type = db.Column(db.String(50), nullable=False)  # e.g., 'health', 'dental', 'vision'
    coverage_level = db.Column(db.String(50))  # e.g., 'individual', 'family', 'premium'
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    requested_start_date = db.Column(db.Date, nullable=False)
    policy_duration = db.Column(db.Integer)  # Duration in months
    monthly_premium = db.Column(db.Float)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    notes = db.Column(db.Text)
    supporting_documents = db.Column(db.Text)  # Could store file paths or references
    
    user = db.relationship('User', backref=db.backref('insurance_applications', lazy=True))
