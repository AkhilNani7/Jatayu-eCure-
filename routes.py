import json
from datetime import datetime, date
from flask import render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Doctor, Medicine, CartItem, Appointment, Prescription, Order, OrderItem
from utils import format_datetime, calculate_total

def init_routes(app, db):
    # APK Download route
    @app.route('/download-apk')
    def download_apk():
        apk_path = 'static/downloads/healthcare.apk'
        return send_file(
            apk_path,
            as_attachment=True,
            download_name='HealthCare-Portal.apk',
            mimetype='application/vnd.android.package-archive'
        )

    # Insurance routes
    @app.route('/insurance')
    @login_required
    def insurance():
        return render_template('insurance.html')

    @app.route('/insurance/submit', methods=['POST'])
    @login_required
    def submit_insurance_application():
        policy_type = request.form.get('policy_type')
        coverage_level = request.form.get('coverage_level')
        requested_start_date = datetime.strptime(request.form.get('requested_start_date'), '%Y-%m-%d').date()
        policy_duration = int(request.form.get('policy_duration'))
        notes = request.form.get('notes')

        application = InsuranceApplication(
            user_id=current_user.id,
            policy_type=policy_type,
            coverage_level=coverage_level,
            requested_start_date=requested_start_date,
            policy_duration=policy_duration,
            notes=notes
        )
        
        db.session.add(application)
        db.session.commit()
        
        flash('Insurance application submitted successfully')
        return redirect(url_for('profile'))

    # Chatbot routes
    @app.route('/chatbot')
    def chatbot():
        return render_template('chatbot.html')
        
    @app.route('/chatbot/message', methods=['POST'])
    def chatbot_message():
        data = request.json
        user_message = data.get('message', '').lower()
        
        # Simple response logic - in a real app, you'd want to use a more sophisticated system
        responses = {
            'headache': "For headaches, try resting in a quiet dark room, stay hydrated, and consider over-the-counter pain relievers. If persistent, consult a doctor.",
            'fever': "For fever, rest well, stay hydrated, and use fever reducers if temperature is high. Seek medical attention if fever persists over 3 days.",
            'cold': "For cold symptoms, get plenty of rest, drink warm fluids, and try over-the-counter cold medications. Use warm salt water gargles for sore throat.",
            'help': "I can help you with common health concerns. Just describe your symptoms or ask health-related questions.",
        }
        
        response = "I'm not sure about that specific issue. Please consult a healthcare professional for accurate medical advice."
        
        for keyword, reply in responses.items():
            if keyword in user_message:
                response = reply
                break
                
        return jsonify({'response': response})

    # Home route
    @app.route('/')
    def index():
        # Fetch recent doctors and medicines for homepage
        doctors = Doctor.query.limit(4).all()
        medicines = Medicine.query.limit(8).all()
        return render_template('index.html', doctors=doctors, medicines=medicines)

    # User Authentication Routes
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('index'))
            else:
                flash('Invalid email or password')
        
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            # Validation
            if password != confirm_password:
                flash('Passwords do not match')
                return render_template('register.html')
            
            if User.query.filter_by(username=username).first():
                flash('Username already exists')
                return render_template('register.html')
            
            if User.query.filter_by(email=email).first():
                flash('Email already exists')
                return render_template('register.html')
            
            # Create new user
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        
        return render_template('register.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        if request.method == 'POST':
            # Update user profile
            current_user.first_name = request.form.get('first_name')
            current_user.last_name = request.form.get('last_name')
            current_user.phone = request.form.get('phone')
            current_user.address = request.form.get('address')
            
            # Parse date of birth if provided
            dob_str = request.form.get('date_of_birth')
            if dob_str:
                try:
                    current_user.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
                except ValueError:
                    flash('Invalid date format for date of birth')
            
            db.session.commit()
            flash('Profile updated successfully')
        
        # Get user's appointments
        appointments = Appointment.query.filter_by(user_id=current_user.id).order_by(Appointment.appointment_date.desc()).limit(5).all()
        # Get user's orders
        orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.order_date.desc()).limit(5).all()
        
        return render_template('profile.html', user=current_user, appointments=appointments, orders=orders)

    # Doctors Routes
    @app.route('/doctors')
    def doctors():
        specialty = request.args.get('specialty')
        
        if specialty:
            doctors = Doctor.query.filter_by(specialty=specialty).all()
        else:
            doctors = Doctor.query.all()
        
        # Get unique specialties for filter dropdown
        specialties = db.session.query(Doctor.specialty).distinct().all()
        specialties = [s[0] for s in specialties]
        
        return render_template('doctors.html', doctors=doctors, specialties=specialties, selected_specialty=specialty)

    @app.route('/doctors/<int:doctor_id>')
    def doctor_detail(doctor_id):
        doctor = Doctor.query.get_or_404(doctor_id)
        available_days = doctor.available_days.split(',') if doctor.available_days else []
        available_times = json.loads(doctor.available_times) if doctor.available_times else {}
        
        return render_template('doctor_detail.html', doctor=doctor, 
                               available_days=available_days, 
                               available_times=available_times)

    # Medicines Routes
    @app.route('/medicines')
    def medicines():
        category = request.args.get('category')
        search = request.args.get('search')
        
        query = Medicine.query
        
        if category:
            query = query.filter_by(category=category)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (Medicine.name.ilike(search_term)) | 
                (Medicine.generic_name.ilike(search_term)) |
                (Medicine.description.ilike(search_term))
            )
        
        medicines = query.all()
        
        # Get unique categories for filter dropdown
        categories = db.session.query(Medicine.category).distinct().all()
        categories = [c[0] for c in categories if c[0]]
        
        return render_template('medicines.html', medicines=medicines, 
                              categories=categories, 
                              selected_category=category,
                              search_term=search)

    @app.route('/medicines/<int:medicine_id>')
    def medicine_detail(medicine_id):
        medicine = Medicine.query.get_or_404(medicine_id)
        # Get related medicines in the same category
        related_medicines = Medicine.query.filter_by(category=medicine.category).filter(Medicine.id != medicine.id).limit(4).all()
        
        return render_template('medicine_detail.html', medicine=medicine, related_medicines=related_medicines)

    # Cart Routes
    @app.route('/cart')
    @login_required
    def cart():
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        total = calculate_total(cart_items)
        
        return render_template('cart.html', cart_items=cart_items, total=total)

    @app.route('/cart/add', methods=['POST'])
    @login_required
    def add_to_cart():
        medicine_id = request.form.get('medicine_id', type=int)
        quantity = request.form.get('quantity', type=int, default=1)
        
        if not medicine_id or quantity <= 0:
            flash('Invalid request')
            return redirect(request.referrer or url_for('medicines'))
        
        medicine = Medicine.query.get_or_404(medicine_id)
        
        # Check if medicine requires prescription
        if medicine.requires_prescription:
            # Check if user has a valid prescription for this medicine
            # This is a simplified check - in a real system you'd check prescription details
            has_prescription = Prescription.query.filter_by(
                user_id=current_user.id,
                status='active'
            ).first() is not None
            
            if not has_prescription:
                flash('This medicine requires a prescription')
                return redirect(request.referrer or url_for('medicine_detail', medicine_id=medicine_id))
        
        # Check stock
        if quantity > medicine.stock_quantity:
            flash(f'Sorry, only {medicine.stock_quantity} units available')
            return redirect(request.referrer or url_for('medicine_detail', medicine_id=medicine_id))
        
        # Check if item is already in cart
        cart_item = CartItem.query.filter_by(
            user_id=current_user.id,
            medicine_id=medicine_id
        ).first()
        
        if cart_item:
            # Update quantity
            cart_item.quantity += quantity
        else:
            # Add new item
            cart_item = CartItem(
                user_id=current_user.id,
                medicine_id=medicine_id,
                quantity=quantity
            )
            db.session.add(cart_item)
        
        db.session.commit()
        flash('Added to cart')
        
        return redirect(request.referrer or url_for('medicines'))

    @app.route('/cart/update', methods=['POST'])
    @login_required
    def update_cart():
        cart_item_id = request.form.get('cart_item_id', type=int)
        quantity = request.form.get('quantity', type=int, default=1)
        
        if not cart_item_id or quantity < 0:
            flash('Invalid request')
            return redirect(url_for('cart'))
        
        cart_item = CartItem.query.get_or_404(cart_item_id)
        
        # Ensure the cart item belongs to the current user
        if cart_item.user_id != current_user.id:
            flash('Unauthorized access')
            return redirect(url_for('cart'))
        
        if quantity == 0:
            db.session.delete(cart_item)
            flash('Item removed from cart')
        else:
            # Check stock
            if quantity > cart_item.medicine.stock_quantity:
                flash(f'Sorry, only {cart_item.medicine.stock_quantity} units available')
                return redirect(url_for('cart'))
            
            cart_item.quantity = quantity
            flash('Cart updated')
        
        db.session.commit()
        
        return redirect(url_for('cart'))

    @app.route('/cart/remove/<int:cart_item_id>', methods=['POST'])
    @login_required
    def remove_from_cart(cart_item_id):
        cart_item = CartItem.query.get_or_404(cart_item_id)
        
        # Ensure the cart item belongs to the current user
        if cart_item.user_id != current_user.id:
            flash('Unauthorized access')
            return redirect(url_for('cart'))
        
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from cart')
        
        return redirect(url_for('cart'))

    # Checkout Routes
    @app.route('/checkout', methods=['GET', 'POST'])
    @login_required
    def checkout():
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        
        if not cart_items:
            flash('Your cart is empty')
            return redirect(url_for('cart'))
        
        total = calculate_total(cart_items)
        
        if request.method == 'POST':
            # Process order
            shipping_address = request.form.get('shipping_address')
            payment_method = request.form.get('payment_method')
            
            if not shipping_address or not payment_method:
                flash('Please fill all required fields')
                return render_template('checkout.html', cart_items=cart_items, total=total)
            
            # Create order
            order = Order(
                user_id=current_user.id,
                total_amount=total,
                shipping_address=shipping_address,
                payment_method=payment_method,
                payment_status='completed'  # In a real app, this would be set after payment processing
            )
            db.session.add(order)
            db.session.flush()  # Get the order ID without committing
            
            # Create order items and update stock
            for cart_item in cart_items:
                order_item = OrderItem(
                    order_id=order.id,
                    medicine_id=cart_item.medicine_id,
                    quantity=cart_item.quantity,
                    price=cart_item.medicine.price
                )
                db.session.add(order_item)
                
                # Update stock
                medicine = cart_item.medicine
                medicine.stock_quantity -= cart_item.quantity
                
                # Remove from cart
                db.session.delete(cart_item)
            
            db.session.commit()
            flash('Order placed successfully!')
            
            return redirect(url_for('profile'))
        
        return render_template('checkout.html', cart_items=cart_items, total=total)

    # Appointment Routes
    @app.route('/appointments')
    @login_required
    def appointments():
        user_appointments = Appointment.query.filter_by(user_id=current_user.id).order_by(Appointment.appointment_date.desc()).all()
        return render_template('appointments.html', appointments=user_appointments)

    @app.route('/book-appointment/<int:doctor_id>', methods=['POST'])
    @login_required
    def book_appointment(doctor_id):
        doctor = Doctor.query.get_or_404(doctor_id)
        appointment_date = request.form.get('appointment_date')
        appointment_time = request.form.get('appointment_time')
        reason = request.form.get('reason')
        is_virtual = request.form.get('is_virtual') == 'on'
        
        if not appointment_date or not appointment_time:
            flash('Please select a date and time')
            return redirect(url_for('doctor_detail', doctor_id=doctor_id))
        
        # Convert string date to date object
        try:
            appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format')
            return redirect(url_for('doctor_detail', doctor_id=doctor_id))
        
        # Check if appointment date is in the future
        if appointment_date < date.today():
            flash('Cannot book an appointment in the past')
            return redirect(url_for('doctor_detail', doctor_id=doctor_id))
        
        # Create appointment
        appointment = Appointment(
            user_id=current_user.id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            reason=reason,
            is_virtual=is_virtual
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        flash('Appointment booked successfully')
        return redirect(url_for('appointments'))

    @app.route('/cancel-appointment/<int:appointment_id>', methods=['POST'])
    @login_required
    def cancel_appointment(appointment_id):
        appointment = Appointment.query.get_or_404(appointment_id)
        
        # Ensure the appointment belongs to the current user
        if appointment.user_id != current_user.id:
            flash('Unauthorized access')
            return redirect(url_for('appointments'))
        
        # Check if appointment is in the future
        if appointment.appointment_date < date.today():
            flash('Cannot cancel past appointments')
            return redirect(url_for('appointments'))
        
        appointment.status = 'cancelled'
        db.session.commit()
        
        flash('Appointment cancelled')
        return redirect(url_for('appointments'))

    # Virtual Consultation
    @app.route('/consultation/<int:appointment_id>')
    @login_required
    def consultation(appointment_id):
        appointment = Appointment.query.get_or_404(appointment_id)
        
        # Ensure the appointment belongs to the current user
        if appointment.user_id != current_user.id:
            flash('Unauthorized access')
            return redirect(url_for('appointments'))
        
        # Ensure the appointment is for a virtual consultation
        if not appointment.is_virtual:
            flash('This is not a virtual consultation')
            return redirect(url_for('appointments'))
        
        # Ensure the appointment is today
        if appointment.appointment_date != date.today():
            if appointment.appointment_date < date.today():
                flash('This appointment has already passed')
            else:
                flash('This appointment is scheduled for the future')
            return redirect(url_for('appointments'))
        
        return render_template('consultation.html', appointment=appointment)

    # Custom template filters
    @app.template_filter('format_datetime')
    def format_datetime_filter(value, format='%Y-%m-%d'):
        return format_datetime(value, format)

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500
